import itertools

import yaml
import random

from cfg_generator import generate_sentences_from_cfg
from conf_reader import ConfReader
from data_reader import DatasetParser
from read_utils import get_vocab


def get_sentence_pairs(sentence_list_1, sentence_list_2):
    # pairs
    pairs = itertools.product(sentence_list_1, sentence_list_2)
    # filtering the pairs
    result = [pair for pair in pairs if pair[0] != pair[1]]
    return result
    # result = random.sample(set(itertools.product(sentence_list_1, sentence_list_2)), 1000)
    # return result


def simple_list_to_cfg_list_convert(simple_list):
    cfg_list = " | ".join(['"{0}"'.format(x) for x in simple_list])
    return cfg_list


def write_vocab_file(vocab_dict, vocab_filename):
    vocab_file_out = open(vocab_filename, "w")
    adj_list = simple_list_to_cfg_list_convert(vocab_dict["J"])
    adj_line = "ADJ -> " + adj_list

    np_list = simple_list_to_cfg_list_convert(vocab_dict["N"])
    np_line = "N -> " + np_list

    vb_list = simple_list_to_cfg_list_convert(vocab_dict["V"])
    vb_line = "VB -> " + vb_list

    vocab_file_out.write(adj_line + "\n" + np_line + "\n" + vb_line)


def intersection(vocab_list):
    return list(set(vocab_list[0]) & set(vocab_list[1]))


def print_vocab_stats(it_vocab, food_vocab):
    verbs = it_vocab["V"], food_vocab["V"]
    nouns = it_vocab["N"], food_vocab["N"]
    adjectives = it_vocab["J"], food_vocab["J"]
    print("Common verbs: ", intersection(verbs))
    print("Common nouns: ", intersection(nouns))
    print("Common adjectives: ", intersection(adjectives))


def conf_reader(conf_file):
    with open(conf_file) as f:
        conf_dic = yaml.load(f, Loader=yaml.FullLoader)
    return conf_dic


def write_final_data_file(filename, data_size, food_syn_sentences, it_syn_sentences):
    model_data_file = open(filename, "w")
    for k in range(data_size):
        food_line_1 = random.choice(food_syn_sentences)
        food_line_2 = random.choice(food_syn_sentences)
        pair_1 = [food_line_1, food_line_2]
        it_line_1 = random.choice(it_syn_sentences)
        it_line_2 = random.choice(it_syn_sentences)
        pair_2 = [it_line_1, it_line_2]

        it_line_3 = random.choice(it_syn_sentences)
        food_line_3 = random.choice(food_syn_sentences)
        pair_3 = [it_line_3, food_line_3]
        random.shuffle(pair_3)
        model_data_file.write("\t".join(pair_1) + "\t" + "1\n")
        model_data_file.write("\t".join(pair_2) + "\t" + "1\n")
        model_data_file.write("\t".join(pair_3) + "\t" + "0\n")
    model_data_file.close()
    return True


if __name__ == '__main__':
    # read config file
    config = ConfReader("conf.yaml")
    # open source data file names
    FOOD_CORPUS = config.food_raw_file
    IT_CORPUS = config.it_raw_file
    # load constants from config
    LIMIT_FOR_VOCAB_LEN = config.limit_for_vocab_length
    MAX_SEN_PER_CORPUS = config.max_sentence_per_corpus
    MAX_DEPTH_FOR_CFG = config.max_depth_cfg
    TOTAL_SENTENCES_PER_GENRE = config.total_utterances
    # read CFG rules file
    CFG_RULES = open(config.cfg_file, "r").read()
    MODEL_DATA_SIZE = config.model_data_size
    MODEL_DATA_FILENAME = config.model_data_file_name
    FOOD_VOCAB_FILENAME = config.food_vocab_file_name
    IT_VOCAB_FILENAME = config.it_vocab_file_name

    data_parser = DatasetParser(FOOD_CORPUS, IT_CORPUS)
    # parse open source files ... method returns list of sentences
    # new loaders can be written in DatasetParser class
    food_sentences, it_sentences = data_parser.foodbase_parser(), data_parser.it_parser()
    # prepare vocab and dump in  NLTK CFG readable format
    food_vocab_dic, it_vocab_dic = get_vocab(food_sentences[:MAX_SEN_PER_CORPUS], LIMIT_FOR_VOCAB_LEN), get_vocab(
        it_sentences[:MAX_SEN_PER_CORPUS], LIMIT_FOR_VOCAB_LEN)

    write_vocab_file(food_vocab_dic, FOOD_VOCAB_FILENAME)
    write_vocab_file(it_vocab_dic, IT_VOCAB_FILENAME)
    print_vocab_stats(it_vocab_dic, food_vocab_dic)

    food_sentences_annotated = generate_sentences_from_cfg(CFG_RULES, FOOD_VOCAB_FILENAME, MAX_DEPTH_FOR_CFG,
                                                           TOTAL_SENTENCES_PER_GENRE)
    it_sentences_annotated = generate_sentences_from_cfg(CFG_RULES, IT_VOCAB_FILENAME, MAX_DEPTH_FOR_CFG,
                                                         TOTAL_SENTENCES_PER_GENRE)
    write_final_data_file(MODEL_DATA_FILENAME, MODEL_DATA_SIZE, food_sentences_annotated, it_sentences_annotated)
