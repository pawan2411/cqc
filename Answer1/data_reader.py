import bioc

import json


class DatasetParser:
    def __init__(self, foodbase_file, it_file):
        self.fb_file = foodbase_file
        self.it_file = it_file

    def foodbase_parser(self):
        all_sentences = []
        fp = open(self.fb_file, 'r')
        collection = bioc.load(fp)
        for doc in collection.documents:
            sentence = (doc.infons["full_text"].strip().lower())
            all_sentences.append(sentence)
        return all_sentences

    def it_parser(self):
        all_sentences = []
        with open(self.it_file) as f:
            for line in f:
                all_sentences.append(json.loads(line)["text"].strip().lower())
        return all_sentences
