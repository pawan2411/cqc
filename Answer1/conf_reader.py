import os
import yaml
import logging

logger = logging.getLogger(__name__)


class ConfReader:
    """read conf parameters from yml conf file for general items
    input: env: environment variable
    """

    def __init__(self, conf_file):
        try:
            with open(conf_file, 'r') as stream:
                config = yaml.safe_load(stream)
            self.food_raw_file = config["create_data"]["food_raw_file"]
            self.it_raw_file = config["create_data"]["it_raw_file"]
            self.limit_for_vocab_length = config["create_data"]["limit_for_vocab_length"]
            self.max_sentence_per_corpus = config["create_data"]["max_sentence_per_corpus"]
            self.cfg_file = config["create_data"]["cfg_file"]
            self.max_depth_cfg = config["create_data"]["max_depth_cfg"]
            self.total_utterances = config["create_data"]["total_utterances"]
            self.food_vocab_file_name = config["create_data"]["food_vocab_file_name"]
            self.it_vocab_file_name = config["create_data"]["it_vocab_file_name"]
            self.model_data_size = config["create_data"]["model_data_size"]
            self.model_data_file_name = config["create_data"]["model_data_file_name"]



        except yaml.YAMLError as exc:
            logger.error(exc)