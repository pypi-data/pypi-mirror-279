import time
import threading
import torch
import numpy as np
from datetime import datetime
from fitxf import FitXformInterface
from nwae.math.datasource.vecdb.model.ModelInterface import ModelInterface, ModelEncoderInterface
from nwae.math.datasource.vecdb.metadata.MetadataInterface import MetadataInterface
from nwae.math.utils.ObjPers import ObjectPersistence
from nwae.math.utils.Profile import Profiling


class ModelStandard(ModelInterface):

    def __init__(
            self,
            user_id: str,
            llm_model: ModelEncoderInterface,
            col_content: str,
            col_label_user: str,
            col_label_std: str,
            col_embedding: str,
            numpy_to_b64_for_db: bool,
            vec_db_metadata: MetadataInterface,
            cache_tensor_to_file: bool,
            file_temp_dir: str,
            fit_xform_model: FitXformInterface,
            # allowed values: "np", "torch"
            return_tensors: str,
            enable_bg_thread_for_training: bool = True,
            logger = None,
    ):
        super().__init__(
            user_id = user_id,
            llm_model = llm_model,
            col_content = col_content,
            col_label_user = col_label_user,
            col_label_std = col_label_std,
            col_embedding = col_embedding,
            numpy_to_b64_for_db = numpy_to_b64_for_db,
            vec_db_metadata = vec_db_metadata,
            fit_xform_model = fit_xform_model,
            cache_tensor_to_file = cache_tensor_to_file,
            file_temp_dir = file_temp_dir,
            return_tensors = return_tensors,
            enable_bg_thread_for_training = enable_bg_thread_for_training,
            logger = logger,
        )

        # 1st time load data
        self.init_data_model(
            max_tries = self.LOAD_DATA_MAX_TRIES_DEFAULT,
            background = False,
        )

        self.check_model_consistency_with_prev()
        self.bg_thread.start()
        return

    def run_bg_thread(
            self,
    ):
        self.logger.info('Model thread started...')
        while True:
            time.sleep(self.bg_thread_sleep_secs)
            if self.signal_stop_bg_thread:
                self.logger.warning('Exiting model thread, stop signal received.')
                break

            if not self.cache_tensor_to_file:
                continue

            # check if need to free memory here
            secs_since_last_active = Profiling(logger=self.logger).get_time_dif_secs(
                start = self.last_active_using_objpers,
                stop = datetime.now(),
                decimals = 4,
            )

            if secs_since_last_active > self.clear_memory_secs_inactive:
                if self.data_n_tensors_in_ram:
                    self.logger.info(
                        'Data & tensors in RAM = ' + str(self.data_n_tensors_in_ram)
                        + ', seconds since last active now ' + str(secs_since_last_active)
                        + ', clearing memory of length ' + str(self.get_data_length()) + ' tensors/records.'
                    )
                    self.free_memory()
                else:
                    self.logger.debug('Data & tensors already not in RAM, not clearing.')

    def init_data_model(
            self,
            max_tries = ModelInterface.LOAD_DATA_MAX_TRIES_DEFAULT,
            background = False,
    ):
        # During initialization, we cannot throw exception. Fail means will depend on primary user cache already.
        required_mutexes = [self.mutex_name_model]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = 'init_data_model',
                mutexes = required_mutexes,
            )
            self.reset_data_model__()
            # let Exceptions throw
        finally:
            self.lock_mutexes.release_mutexes(mutexes=required_mutexes)

        # If error loading data, should die and throw exception
        self.load_data_model(max_tries=max_tries, background=background)
        return

    def load_data_model(
            self,
            max_tries = ModelInterface.LOAD_DATA_MAX_TRIES_DEFAULT,
            background = False,
    ):
        return self.sync_model_with_underlying_db(
            max_tries = max_tries,
            background = background,
        )

    def update_model(
            self,
            force_update = False,
    ):
        return self.load_data_model()

    def reset_data_model__(
            self,
    ):
        super().reset_data_model__()
        #
        # Default "built-in filesystem" model parameters required for inference
        #
        # In truth these maps are not required for this simple dense model, but we keep it anyway
        # since all other proper math models (e.g. NN) will always need mapping labels to numbers.
        self.map_lbl_to_idx = {}
        self.map_idx_to_lbl = {}
        self.text_encoded = np.array([])    # the initial shape is not correct anyway, but doesn't matter
        self.text_labels_standardized = np.array([])
        self.data_records = []

        # Store in file instead of memory for potentially large objects
        self.text_encoded_objpers_filepath = self.file_name_prefix + '__text_encoded.b'
        self.text_encoded_objpers_lockpath = self.file_name_prefix + '__text_encoded.lock'
        self.text_encoded_objpers = ObjectPersistence(
            default_obj = [],
            obj_file_path = self.text_encoded_objpers_filepath,
            lock_file_path = self.text_encoded_objpers_lockpath,
            logger = self.logger,
        )
        # Store in file instead of memory for potentially large objects
        self.data_records_objpers_filepath = self.file_name_prefix + '__data_records.b'
        self.data_records_objpers_lockpath = self.file_name_prefix + '__data_records.lock'
        self.data_records_objpers = ObjectPersistence(
            default_obj = [],
            obj_file_path = self.data_records_objpers_filepath,
            lock_file_path = self.data_records_objpers_lockpath,
            logger = self.logger,
        )
        self.last_active_using_objpers = datetime.now()
        self.data_n_tensors_in_ram = False

        self.set_high_urgency_to_sync_with_underlying_db()
        self.logger.info(
            'Model params reset with last load time set to 2000, so that cache will urgently reload'
        )
        return

    # lock must already be obtained before calling any functions with "__"
    def __deserialize_objects(self):
        if not self.cache_tensor_to_file:
            return
        if self.data_n_tensors_in_ram:
            return
        self.last_active_using_objpers = datetime.now()
        text_encoded_array = self.text_encoded_objpers.deserialize_object_from_file(
            # max_wait_time_secs = ,
        )
        self.text_encoded = np.array(text_encoded_array)
        data_records_array = self.data_records_objpers.deserialize_object_from_file(
            # max_wait_time_secs = ,
        )
        self.data_records = data_records_array
        # signal that memory is now in RAM
        self.data_n_tensors_in_ram = True
        return

    # lock must already be obtained before calling any functions with "__"
    def __serialize_objects(self):
        if not self.cache_tensor_to_file:
            return
        self.text_encoded_objpers.serialize_object_to_file(
            obj = self.text_encoded.tolist(),
            # max_wait_time_secs =,
        )
        self.data_records_objpers.serialize_object_to_file(
            obj = self.data_records,
            # max_wait_time_secs = ,
        )
        return

    def free_memory(self):
        if not self.cache_tensor_to_file:
            return

        required_mutexes = [self.mutex_name_model, self.mutex_name_underlying_db]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = 'free_memory',
                mutexes = required_mutexes,
            )
            self.__free_memory()
            self.logger.info('Memory successfully freed')
        except Exception as ex:
            self.logger.error('Error releasing memory: ' + str(ex))
        finally:
            self.lock_mutexes.release_mutexes(mutexes=required_mutexes)
        return

    # lock must already be obtained before calling any functions with "__"
    def __free_memory(self):
        del self.text_encoded
        del self.data_records
        self.text_encoded = np.array([])
        self.data_records = []
        self.data_n_tensors_in_ram = False
        self.logger.info('Data & tensors cleared from memory')
        return

    def atomic_delete_add(
            self,
            delete_key: str,
            # list of dicts
            records: list[dict],
    ):
        assert len(records) > 0, 'No records to train'

        self.logger.info(
            'Records of length ' + str(len(records)) # + ', background train mode = ' + str(train_in_background)
        )

        required_mutexes = [self.mutex_name_model, self.mutex_name_underlying_db]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = 'atomic_delete_add',
                mutexes = required_mutexes,
            )
            self.__deserialize_objects()

            #
            # Train 1st Part: Model variables in memory
            #
            for rec in records:
                text_encoded_rec = self.calc_embedding(
                    content_list = [rec[self.col_content]],
                    # max_tokens = max_tokens,
                    # return_tensors = self.RETURN_TENSORS,
                )
                self.logger.info(
                    'Text encoded using lm model "' + str(self.llm_model.get_model_name()) + '" with shape '
                    + str(text_encoded_rec.shape if self.return_tensors == 'np' else text_encoded_rec.size())
                )

                assert delete_key in rec.keys(), \
                    'Delete key "' + str(delete_key) + '" not in record keys ' + str(rec.keys())
                mp = [{delete_key: rec[delete_key]}]
                self.logger.info('Trying to delete using match phrase ' + str(mp))
                self.__delete_records_from_model(match_phrases=mp)
                self.delete_records_from_underlying_db__(match_phrases=mp)

                records_with_embedding_and_labelstd = self.update_label_maps_from_new_recs__(
                    records = [rec],
                    text_encoding_tensor = text_encoded_rec,
                )
                self.add_records_to_underlying_db__(
                    records_with_embedding_and_labelstd = records_with_embedding_and_labelstd,
                )

            self.__serialize_objects()

            # At this point, model is updated, with new/deleted data. So we need to update metadata
            self.update_metadata_db_data_updated()
            return True
        except Exception as ex:
            self.logger.error(
                'Exception in atomic delete add adding records: ' + str(records) + '. Got exception ' + str(ex)
            )
            raise Exception(ex)
        finally:
            self.lock_mutexes.release_mutexes(mutexes=required_mutexes)

    def ____check_model_params_consistency(
            self,
    ):
        assert self.lock_mutexes.is_locked(mutex=self.mutex_name_model)
        try:
            assert len(self.text_encoded) == len(self.text_labels_standardized), \
                'Inconsistent lengths encoding ' + str(len(self.text_encoded)) \
                + ' labels ' + str(len(self.text_labels_standardized))
            assert len(self.text_encoded) == len(self.data_records), \
                'Inconsistent lengths encoding ' + str(len(self.text_encoded)) \
                + ' training records ' + str(len(self.data_records))
            self.logger.debug('Consistency check tensor/record lengths consistent, length ' + str(len(self.text_encoded)))

            type_check = np.ndarray if self.return_tensors == 'np' else torch.Tensor
            assert type(self.text_encoded) is type_check,\
                'Wrong type for encoded text "' + str(type(self.text_encoded)) + '"'
            if len(self.text_encoded) > 0:
                assert type(self.text_encoded[0]) is type_check, \
                    'Wrong type for encoded text index 0 "' + str(type(self.text_encoded[0])) + '"'
            self.logger.debug('Consistency check embedding tensor type ok, of type ' + str(type_check))

            user_labels_in_maps = list(np.unique([lbl for lbl in self.map_lbl_to_idx.keys()]))
            std_labels_in_maps = list(np.unique([lbl for lbl in self.map_idx_to_lbl.keys()]))
            # self.logger.info(
            #     'Training record columns: ' + str(pd.DataFrame(self.data_records).columns)
            #     + ', user labels ' + str(user_labels_in_maps) + ', std labels ' + str(std_labels_in_maps)
            #     + ', label user column name "' + str(self.col_label_user) + '"'
            # )
            # Don't throw exception for these non-critical errors, just log error
            missing_indexes = []
            for i in self.text_labels_standardized:
                if i not in std_labels_in_maps:
                    missing_indexes.append(i)
            if missing_indexes:
                self.logger.warning('Missing indexes ' + str(missing_indexes) + ' in ' + str(std_labels_in_maps))
            missing_labels = []
            for lbl in [row[self.col_label_user] for row in self.data_records]:
                if lbl not in user_labels_in_maps:
                    missing_labels.append(lbl)
            if missing_labels:
                self.logger.warning('Missing user labels ' + str(missing_labels) + ' in ' + str(user_labels_in_maps))
            self.logger.debug('Consistency check maps ok, user labels count ' + str(len(user_labels_in_maps)))
        except Exception as ex:
            self.logger.critical('Critical error with model consistency: ' + str(ex))
            self.reset_data_model__()
        return

    def add(
            self,
            # list of dicts
            records: list,
    ):
        assert len(records) > 0, 'No records to train'
        self.logger.info('Add records of length ' + str(len(records)))

        text_encoded_save = self.calc_embedding(
            content_list = [r[self.col_content] for r in records],
        )
        self.logger.info(
            'Text encoded using lm model "' + str(self.llm_model.get_model_name()) + '" with shape '
            + str(text_encoded_save.shape if self.return_tensors == 'np' else text_encoded_save.size())
        )

        done_model_update = False
        done_db_update = False

        required_mutexes = [self.mutex_name_model, self.mutex_name_underlying_db]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = 'model_update_add',
                mutexes = required_mutexes,
            )
            self.__deserialize_objects()

            records_with_embedding_and_labelstd = self.update_label_maps_from_new_recs__(
                records = records,
                text_encoding_tensor = text_encoded_save,
            )

            if len(records) > 0:
                self.____add_records_to_model(
                    records_no_embedding = records,
                    text_encoded_to_update = text_encoded_save,
                )
            else:
                self.logger.warning('Not updating model files, no encoded text')

            done_model_update = True

            #
            # Train 2nd Part: Update new records to canonical primary user cache
            #
            self.add_records_to_underlying_db__(
                records_with_embedding_and_labelstd = records_with_embedding_and_labelstd,
            )
            done_db_update = True
            self.__serialize_objects()

            # At this point, model is updated, with new/deleted data. So we need to update metadata
            self.update_metadata_db_data_updated()
            return True
        except Exception as ex:
            if not done_model_update:
                self.set_high_urgency_to_sync_with_underlying_db()
                errmsg = 'Error occurred during model update: ' + str(ex)
            elif not done_db_update:
                errmsg = 'Error occurred during underlying DB update: ' + str(ex)
            else:
                errmsg = 'Error occurred during model metadata update for add: ' + str(ex)
            self.logger.error(errmsg)
            raise Exception(errmsg)
        finally:
            self.lock_mutexes.release_mutexes(mutexes=required_mutexes)

    def delete(
            self,
            match_phrases,
    ):
        self.logger.info('Delete records for match phrases ' + str(match_phrases))
        done_model_update = False
        done_db_update = False

        required_mutexes = [self.mutex_name_model, self.mutex_name_underlying_db]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = 'delete',
                mutexes = required_mutexes,
            )
            self.__deserialize_objects()

            self.__delete_records_from_model(
                match_phrases = match_phrases,
            )
            done_model_update = True

            self.logger.info('Now proceed to delete from underlying DB..')
            total_deleted = self.delete_records_from_underlying_db__(
                match_phrases = match_phrases,
            )
            done_db_update = True
            self.__serialize_objects()

            # At this point, model is updated, with new/deleted data. So we need to update metadata
            self.update_metadata_db_data_updated()
            return True
        except Exception as ex:
            if not done_model_update:
                self.set_high_urgency_to_sync_with_underlying_db()
                errmsg = 'Error occurred during model delete: ' + str(ex)
            elif not done_db_update:
                errmsg = 'Error occurred during underlying DB delete: ' + str(ex)
            else:
                errmsg = 'Error occurred during model metadata update for delete: ' + str(ex)
            self.logger.error(errmsg)
            raise Exception(errmsg)
        finally:
            self.lock_mutexes.release_mutexes(mutexes=required_mutexes)

    def predict(
            self,
            text_list_or_embeddings,
            top_k = 5,
            # Instead of just returning the user labels, return full record. Applicable to some models only
            return_full_record = False,
    ):
        # Check to see if we need to sync with underlying DB
        self.sync_model_with_underlying_db(background=False)

        txt_lm = self.convert_to_embeddings_if_necessary(
            text_list_or_embeddings = text_list_or_embeddings,
        )

        required_indexes = [self.mutex_name_model]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = 'predict',
                mutexes = required_indexes,
            )
            self.__deserialize_objects()

            return self.__predict(
                embeddings = txt_lm,
                ref_text_encoded_tensor = self.text_encoded,
                ref_labels_std_tensor = self.text_labels_standardized,
                ref_full_data_records = self.data_records,
                top_k = top_k,
                return_full_record = return_full_record,
                similarity_type = "cosine",
            )
        finally:
            self.lock_mutexes.release_mutexes(mutexes=required_indexes)

    def __predict(
            self,
            embeddings,
            ref_text_encoded_tensor,
            ref_labels_std_tensor,
            ref_full_data_records,
            top_k = 5,
            # Instead of just returning the user labels, return full record. Applicable to some models only
            return_full_record = False,
            # permitted values "cosine", "distance"
            similarity_type = 'cosine',
    ):
        assert self.lock_mutexes.is_locked(mutex=self.mutex_name_model), \
            'Mutex model must be locked by caller to enter this function'

        tsr_type = np.ndarray if self.return_tensors == 'np' else torch.Tensor
        assert type(ref_text_encoded_tensor) is tsr_type, 'Type "' + str(type(ref_text_encoded_tensor)) + '"'
        assert type(embeddings) is tsr_type, 'Type "' + str(type(embeddings)) + '"'

        """
        result_ordered returns 2D matrix, each row represents the closest indexes of ref ordered
        So means if the row is [5, 0, 1, 3, 2, 4], means that the closest match is index 5 in ref,
        2nd closest is index 0 in ref, and so on.
        m_dot_ordered is the result of the dot product, a value of magnitude equal or less than 1.
        """
        self.logger.info('For prediction, using similarity type "' + str(similarity_type) + '"')
        if similarity_type == 'distance':
            result_ordered, m_dot_ordered = self.tensor_utils.similarity_distance(
                x = embeddings,
                ref = ref_text_encoded_tensor.copy(),
                return_tensors = self.return_tensors,
            )
        else:
            result_ordered, m_dot_ordered = self.tensor_utils.dot_sim(
                x = embeddings,
                ref = ref_text_encoded_tensor.copy(),
                return_tensors = self.return_tensors,
            )

        if return_full_record:
            pred_records = [[ref_full_data_records[i] for i in np_row] for np_row in result_ordered]
            pred_probs_list = m_dot_ordered.tolist()

            return [ar[0:min(top_k, len(ar))] for ar in pred_records], \
                [ar[0:min(top_k, len(ar))] for ar in pred_probs_list]
        else:
            pred_labels_standardized = ref_labels_std_tensor[result_ordered]
            # Same interface tolist() for both numpy & torch
            labels_standardized_list = pred_labels_standardized.tolist()

            pred_labels_text_list = [[self.map_idx_to_lbl[i] for i in row] for row in labels_standardized_list]
            pred_probs_list = m_dot_ordered.tolist()

            return [ar[0:min(top_k, len(ar))] for ar in pred_labels_text_list], \
                [ar[0:min(top_k, len(ar))] for ar in pred_probs_list]

    def ____add_records_to_model(
            self,
            records_no_embedding,
            text_encoded_to_update,
    ):
        assert len(records_no_embedding) == len(text_encoded_to_update), \
            'Length records ' + str(len(records_no_embedding)) + ' not length embedding ' + str(len(text_encoded_to_update))

        # Precautionary check before doing updates, although unlikely model is corrupted even before update
        self.____check_model_params_consistency()

        self.logger.info(
            'Encoded text of shape ' + str(text_encoded_to_update.shape)
            + ', will append to model encoded text of shape' + str(self.text_encoded.shape)
        )
        lbl_list_mapped_updated = [r[self.col_label_standardized] for r in records_no_embedding]

        if len(self.text_encoded) == 0:
            text_encoded_updated = text_encoded_to_update
            text_labels_standardized_updated = np.array(lbl_list_mapped_updated)
        else:
            if self.return_tensors == 'np':
                text_encoded_updated = np.append(self.text_encoded, text_encoded_to_update, axis=0)
                text_labels_standardized_updated = np.append(
                    self.text_labels_standardized, np.array(lbl_list_mapped_updated, dtype=int),
                    axis = 0,
                )
            else:
                text_encoded_updated = torch.cat((self.text_encoded, text_encoded_to_update), 0)
                text_labels_standardized_updated = torch.cat(
                    (self.text_labels_standardized, torch.LongTensor(lbl_list_mapped_updated)), 0
                )
        training_records_updated = self.data_records + records_no_embedding

        self.text_encoded = text_encoded_updated
        self.text_labels_standardized = text_labels_standardized_updated
        self.data_records = training_records_updated

        self.logger.info(
            'ADD: Successfully updated model files, new text encoded shape ' + str(self.text_encoded.shape)
            + ', text labels std shape ' + str(self.text_labels_standardized.shape)
            + ', training records length ' + str(len(self.data_records))
        )
        self.____check_model_params_consistency()
        return

    def __delete_records_from_model(
            self,
            match_phrases,
    ):
        # Find indexes of entries to be deleted
        self.logger.info('Trying to delete records by match_phrases: ' + str(match_phrases))
        del_indexes = []
        for mp in match_phrases:
            assert len(mp) == 1, 'Not supported delete with more than 1 key phrase ' + str(mp)
            del_key = list(mp.keys())[0]
            del_val = list(mp.values())[0]
            self.logger.debug(
                'Searching for delete key "' + str(del_key) + '", value "' + str(del_val) + '"'
            )
            # TODO In-elegant loop
            for i, trec in enumerate(self.data_records):
                if trec[del_key] == del_val:
                    if i not in del_indexes:
                        del_indexes.append(i)
                    self.logger.info(
                        'Found delete key "' + str(del_key) + '", value "' + str(del_val)
                        + '" at index #' + str(i) + ', full record: '
                        + str({k:v for k,v in trec.items() if k != self.col_embedding})
                    )
                    break

        np_cond_keep = np.array([i not in del_indexes for i in list(range(len(self.text_encoded)))])
        if len(np_cond_keep) > 0:
            self.logger.debug('Delete: numpy condition to keep: ' + str(np_cond_keep))
            assert len(np_cond_keep) == len(self.text_encoded), \
                'Boolean index length ' + str(len(np_cond_keep)) + ' not match arr length ' + str(self.text_encoded)
            self.text_encoded = self.text_encoded[np_cond_keep]
            self.text_labels_standardized = self.text_labels_standardized[np_cond_keep]
            self.data_records = [
                r for i, r in enumerate(self.data_records) if i not in del_indexes
            ]

            self.logger.info(
                'DELETE: Successfully updated model files with ' + str(len(del_indexes))
                + ' deletions, using match phrases ' + str(match_phrases)
                + ', remain lengths encoding ' + str(len(self.text_encoded))
                + ', labels ' + str(len(self.text_labels_standardized))
                + ', training records ' + str(len(self.data_records))
            )
            self.____check_model_params_consistency()
        else:
            self.logger.warning('Deleting all using match phrases ' + str(match_phrases))
            self.reset_data_model__()

    def __process_records_from_underlying_db(
            self,
            records_from_db,
    ):
        required_mutexes = [self.mutex_name_model, self.mutex_name_underlying_db]
        try:
            self.lock_mutexes.acquire_mutexes(
                id = '__process_records_from_underlying_db',
                mutexes = required_mutexes,
            )

            self.data_records = records_from_db

            # save to class property
            pair_labels_std_user = [
                (r[self.col_label_standardized], r[self.col_label_user])
                for r in self.data_records
            ]
            self.map_idx_to_lbl = {i: lbl for i, lbl in pair_labels_std_user}
            self.map_lbl_to_idx = {lbl: i for i, lbl in self.map_idx_to_lbl.items()}

            # Extract out embedding by pop(), so that it is no longer in training records
            text_encoded = self.get_text_encoding_from_db_records(db_records=self.data_records)
            lbl_list_mapped = [r[self.col_label_standardized] for r in self.data_records]

            if self.return_tensors == 'np':
                self.text_encoded = text_encoded
                self.text_labels_standardized = np.array(lbl_list_mapped, dtype=int)
            else:
                self.text_encoded = torch.Tensor(text_encoded)
                self.text_labels_standardized = torch.LongTensor(lbl_list_mapped)

            self.last_sync_time_with_underlying_db = self.vec_db_metadata.get_metadata_db_data_last_update()
            if self.last_sync_time_with_underlying_db is None:
                self.logger.warning('Last update time from metadata returned None')
                self.last_sync_time_with_underlying_db = self.OLD_DATETIME

            self.logger.info(
                'Done sync to DB ' + str(self.model_db.get_db_params().get_db_info())
                + ', encode embedding to base 64 = ' + str(self.numpy_to_b64_for_db)
                + ', text encoded length ' + str(len(self.text_encoded))
                + ', label length ' + str(len(self.text_labels_standardized))
                + ', updated last sync time DB to "' + str(self.last_sync_time_with_underlying_db) + '"'
            )
            self.____check_model_params_consistency()
            self.data_n_tensors_in_ram = True
            self.__serialize_objects()
        finally:
            self.lock_mutexes.release_mutexes(
                mutexes = required_mutexes,
            )

    def sync_model_with_underlying_db(
            self,
            max_tries = ModelInterface.LOAD_DATA_MAX_TRIES_DEFAULT,
            background = False,
    ):
        # Update model variables from canonical data cache
        self.__load_model_from_underlying_db(
            max_tries = max_tries,
            background = background,
        )
        return

    def is_loading_model_from_underlying_db(self):
        return self.lock_mutexes.is_locked(mutex=self.mutex_name_underlying_db)

    def __load_model_from_underlying_db(
            self,
            max_tries = ModelInterface.LOAD_DATA_MAX_TRIES_DEFAULT,
            background = False,
    ):
        # Laading from cache is a heavy operation, so we try to optimize the timings we do this
        if not self.is_need_to_sync_model_with_db():
            self.logger.info(
                'Model is up to date, last update DB time "' + str(self.last_sync_time_with_underlying_db)
                + '". No need to load model from DB. Skipping this round'
            )
            return

        if self.lock_mutexes.is_locked(mutex=self.mutex_name_underlying_db):
            self.logger.info('Mutex load model from DB is locked. Skipping this round')
            return

        if background:
            raise Exception('Not supported background load')
            job = threading.Thread(
                target = self.vec_db_underlying_data.load_model_from_underlying_db_with_max_retries,
                args = [required_mutexes, max_tries],
            )
            job.start()
            self.logger.info(
                'Possibly slow job to load model data from data cache started, running = '
                + str(self.is_loading_model_from_underlying_db()) + ''
            )
        else:
            all_records = self.model_db.load_model_from_underlying_db_with_max_retries(
                max_tries = max_tries,
            )
            self.__process_records_from_underlying_db(records_from_db=all_records)
            return


if __name__ == '__main__':
    exit(0)
