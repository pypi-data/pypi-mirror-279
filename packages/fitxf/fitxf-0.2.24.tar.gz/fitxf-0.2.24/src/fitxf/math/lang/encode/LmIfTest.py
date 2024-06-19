import logging
from nwae.math.utils.Singleton import Singleton
from nwae.math.lang.encode.LangModelPtSingleton import LangModelPtSingleton, LangModelInterface


class LangModelInterfaceTest:

    def __init__(self, logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        return

    def test(self):
        self.test_singleton(
            ClassType = LangModelInterface,
        )
        return

    def test_singleton(
            self,
            ClassType,
            uniq_models_names = ('model_1', 'model_2', 'model_3',),
            cache_folder = None,
    ):
        try:
            sg_store = Singleton.SINGLETON_STORE_BY_CLASSTYPE[ClassType]
            initial_count = len(sg_store)
        except:
            initial_count = 0
        modulo = len(uniq_models_names)
        for i in range(10):
            # Unique key only includes model name & cache folder, lang is ignored
            obj, key = LangModelPtSingleton.get_singleton(
                LmClass = ClassType,
                model_name = uniq_models_names[i % modulo],
                cache_folder = cache_folder,
                include_tokenizer = False,
                logger = None,
                return_key = True,
            )
            sg_store = Singleton.SINGLETON_STORE_BY_CLASSTYPE[ClassType]
            assert len(sg_store) - initial_count == min(modulo, i+1), \
                'Total objects at index ' + str(i) + ' == ' + str(len(sg_store) - initial_count)
            # print(sg_store, key)
            assert id(obj) == id(sg_store[key]), \
                'Object #' + str(i) + ' must be object ' + str(id(sg_store[key])) + ' with key id "' + str(key) + '"'
            # print(obj)
        print('ALL TESTS PASSED OK')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    o = LangModelInterfaceTest()

    # o.test_discover_max_len(
    #     lang = 'en',
    #     random_txt = LangModelInterface.RANDOM_TEXT,
    # )
    o.test_singleton(ClassType=LangModelInterface)
    exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    o = LangModelInterfaceTest()

    # o.test_discover_max_len(
    #     lang = 'en',
    #     random_txt = LangModelInterface.RANDOM_TEXT,
    # )
    o.test_singleton(ClassType=LangModelInterface)
    exit(0)
