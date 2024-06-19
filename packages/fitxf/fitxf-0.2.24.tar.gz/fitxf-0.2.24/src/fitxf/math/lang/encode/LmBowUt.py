import torch
import logging
import unittest
from nwae.math.lang.encode.LangModelBow import LangModelBow


class LangModelBowUnitTest(unittest.TestCase):

    def test_template(
            self,
            lang,
            tests,
            expected_word_list,
            expected_embeddings = None,
            test_tokenization = True,
            wordlist_extension = None,
            normalize_lm = False,
            logger = None,
    ):
        logger = logger if logger is not None else logging.getLogger()
        lm = LangModelBow(lang=lang)

        txtlist = [p[0] for p in tests]
        embedding = lm.encode(
            text_list = txtlist,
            params_other = {'wordlist_extension': wordlist_extension, 'normalize_lm': normalize_lm},
        )
        logger.debug('Calculated embedding for texts: ' + str(txtlist) + '\n\r' + str(embedding))
        if expected_embeddings is not None:
            test_var = embedding - expected_embeddings
            test_var = test_var * test_var
            test_sum = torch.sum(test_var)
            self.assertTrue(
                test_sum < 1.e-06,
                msg      ='Sum ' + str(test_sum) + '. Observed embedding ' + str(embedding) + ' expected ' + str(expected_embeddings)
            )

        wl = lm.get_bow_word_list()
        self.assertTrue(
            expr = wl == expected_word_list,
            msg = 'Lang ' + str(lang) + ' observed word list ' + str(wl) + ', expected ' + str(expected_word_list)
        )

        if not test_tokenization:
            return

        for test in tests:
            txt_tok = lm.tokenize(text = test[0], return_type='spacy')
            sent_tok = [t.text for t in txt_tok]
            self.assertTrue(
                expr = sent_tok == test[1],
                msg = 'Check ' + str(sent_tok) + ' against expected tokenization ' + str(test[1])
            )

    def test_zh(self):
        tests = (
            ('I love love McD', []),
            ('我爱马克地', []),
            ('Ya liubliu "Vkusna e tochka"', []),
        )
        expected_embedding = torch.FloatTensor([
            [0., 1., 0., 2., 1., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1.],
            [1., 0., 1., 0., 0., 1., 1., 1., 0., 0., 0., 0.],
        ])
        self.test_template(
            lang = 'zh',
            tests = tests,
            expected_word_list = [
                'e', 'i', 'liubliu', 'love', 'mcd', 'tochka"', 'vkusna', 'ya', '地', '我', '爱', '马克',
            ],
            expected_embeddings = expected_embedding,
            test_tokenization = False,
            wordlist_extension = None,
            normalize_lm = False,
        )
        """
        Test with own word list
        """
        tests = (
            ('I love love McD', []),
            ('我爱马克地', []),
            ('Ya liubliu "Vkusna e tochka"', []),
            ('what is nlp', []),
        )
        wlist_ext = ['i', 'love', 'mcd', '我', '爱', 'ya', 'liubliu', 'vkusna']
        expected_embedding = torch.FloatTensor([
            [0.4082, 0.8165, 0.4082, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.7071, 0.7071, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.5774, 0.5774, 0.5774],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
        ])
        self.test_template(
            lang = 'zh',
            tests = tests,
            expected_word_list = ['i', 'love', 'mcd', '我', '爱', 'ya', 'liubliu', 'vkusna'],
            expected_embeddings = expected_embedding,
            test_tokenization = False,
            wordlist_extension = wlist_ext,
            normalize_lm = True,
        )

    def test_th(self):
        tests = [
            ('แผนกนี้กำลังเผชิญกับความท้าทายใหม่', ['แผนก', 'นี้', 'กำลัง', 'เผชิญ', 'กับ', 'ความ', 'ท้าทาย', 'ใหม่']),
            ('ชมสดบอลไทย "ทีมชาติซีเรีย" ลงสนามพบกับ "ทีมชาติไทย"', ['ชม', 'สด', 'บอล', 'ไทย', '"', 'ทีม', 'ชาติ', 'ซีเรีย', '"', 'ลงสนาม', 'พบ', 'กับ', '"', 'ทีม', 'ชาติ', 'ไทย', '"'])
        ]
        expected_embedding = torch.FloatTensor([
            [1., 1., 1., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 1., 1., 1., 0.],
            [1., 0., 0., 1., 2., 1., 2., 0., 0., 1., 1., 1., 1., 0., 0., 0., 2.],
        ])
        self.test_template(
            lang  = 'th',
            tests = tests,
            expected_word_list  = [
                'กับ', 'กำลัง', 'ความ', 'ชม', 'ชาติ', 'ซีเรีย', 'ทีม', 'ท้าทาย', 'นี้', 'บอล', 'พบ',
                'ลงสนาม', 'สด', 'เผชิญ', 'แผนก', 'ใหม่', 'ไทย',
            ],
            expected_embeddings = expected_embedding,
            test_tokenization   = True,
            wordlist_extension  = None,
            normalize_lm        = False,
        )

    def test_vi(self):
        tests = [
            (
                'Hành động chính trị can đảm thể hiện cá tính được ăn thua chịu của một Tổng thống trẻ.',
                [],
            ),
            (
                'Năm đầy rủi ro mở đầu nhiệm kỳ hai của Macron sẽ trả lời câu hỏi là, 4 năm còn lại ông sẽ chèo chống ra sao để lãnh đạo đất nước ?',
                [],
            )
        ]
        expected_word_list = [
            ',', '.', '4', '?', 'can', 'chèo', 'chính', 'chịu', 'chống', 'cá', 'câu', 'còn', 'của', 'hai', 'hiện',
            'hành', 'hỏi', 'kỳ', 'là', 'lãnh', 'lại', 'lời', 'macron', 'một', 'mở', 'nhiệm', 'năm', 'nước', 'ra',
            'ro', 'rủi', 'sao', 'sẽ', 'thua', 'thể', 'thống', 'trả', 'trẻ', 'trị', 'tính', 'tổng', 'ông', 'ăn',
            'động', 'được', 'đạo', 'đảm', 'đất', 'đầu', 'đầy', 'để',
        ]
        self.test_template(
            lang  = 'vi',
            tests = tests,
            expected_word_list  = expected_word_list,
            expected_embeddings = None,
            test_tokenization   = True,
            wordlist_extension  = None,
            normalize_lm        = False,
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    lmb_ut = LangModelBowUnitTest()
    lmb_ut.test_zh()
    lmb_ut.test_th()
    # TODO vi
    # lmb_ut.test_vi()

