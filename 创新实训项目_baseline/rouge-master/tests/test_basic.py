from unittest import TestCase

import rouge
import json


class BasicTest(TestCase):
    def setUp(self):
        self.hyp_path = './hyp.txt'
        self.ref_path = './ref.txt'
        self.rouge = rouge.Rouge()
        self.files_rouge = rouge.FilesRouge(self.hyp_path, self.ref_path)

    def test_one_sentence(self):
        scores = self.files_rouge.get_scores()
        print(scores)
