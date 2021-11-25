import re
from collections import Counter

import nltk

from nltk.tokenize import sent_tokenize


def pos_tagging(txt):
    # print(txt)
    tokenized = sent_tokenize(txt)
    for token in tokenized:
        wordsList = nltk.word_tokenize(token)
        tagged = nltk.pos_tag(wordsList)
        tagged_n_v = []
        for t in tagged:
            if t[1].startswith("N") or t[1].startswith('V') or t[1].startswith('JJ'):
                tagged_n_v.append(t)
        return tagged_n_v


def get_vocab(sentences, limit_for_vocab_length):
    grammar_dic = {}
    vocab_dic = {}
    for sentence in sentences:
        local_dic = (pos_tagging(sentence))
        if local_dic == None:
            continue
        for k in local_dic:
            val, key = k[0], k[1][0]
            if key not in grammar_dic:
                grammar_dic[key] = [val]
            else:
                grammar_dic[key] = grammar_dic[key] + [val]
    for k, v in grammar_dic.items():
        v = Counter(v).most_common(limit_for_vocab_length)
        top_word_list = [i[0] for i in v]
        vocab_dic[k] = top_word_list
    return vocab_dic
