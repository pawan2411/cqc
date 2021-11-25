import json

from nltk import CFG
from nltk.parse.generate import generate, demo_grammar


def generate_sentences_from_cfg(cfg, vocab_file, max_depth, total_utterances):
    adjective_file = open(vocab_file, "r")
    adj = adjective_file.read()
    grammar = CFG.fromstring(cfg + adj)
    all_cfg_sentences = []
    for sentence in generate(grammar, depth=max_depth, n=total_utterances):
        all_cfg_sentences.append(' '.join(sentence))
    return all_cfg_sentences
