import logging
from nwae.math.lang.encode.LangModelPt import LangModelPt as LmPt

class LmPtHfInfo:

    HF_FILES_INFO = {
        LmPt.LM_ST_MULTILINGUAL_MINILM_L12_V2: {
            '.': ('README.md', 'config.json', 'config_sentence_transformers.json', 'model.safetensors',
                  'modules.json', 'pytorch_model.bin', 'sentence_bert_config.json', 'sentencepiece.bpe.model',
                  'special_tokens_map.json', 'tf_model.h5', 'tokenizer.json', 'tokenizer_config.json', 'unigram.json'),
            '1_Pooling': ('config.json',),
        },
        LmPt.LM_INTFL_MULTILINGUAL_E5_SMALL: {
            '.': ('README.md', 'config.json', 'model.safetensors', 'modules.json', 'pytorch_model.bin',
                  'sentence_bert_config.json', 'sentencepiece.bpe.model', 'special_tokens_map.json',
                  'tokenizer.json', 'tokenizer_config.json'),
            '1_Pooling': ('config.json',),
            'onnx': ('config.json', 'model.onnx', 'sentencepiece.bpe.model', 'special_tokens_map.json',
                     'tokenizer.json', 'tokenizer_config.json'),
        },
    }
