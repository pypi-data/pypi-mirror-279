import json
import pickle
from pkgutil import get_data

config_folder, data_folder = 'generichelpers.configs', 'generichelpers.data'
CONFIG = json.loads(get_data(config_folder, 'config.json').decode())
ENGLISH_WORDS = set(pickle.loads(get_data(data_folder, 'english_words.p'))["ENGLISH_WORDS"])
HEADERS = {'Content-Type': 'application/json'}

# Bucket dict
BUCKET_DICT = {
    1: ["0-50", "Small"],
    2: ["50-250", "Small"],
    3: ["250-500", "Small"],
    4: ["500-1K", "Medium"],
    5: ["1K-5K", "Medium"],
    6: ["5K-10K", "Medium"],
    7: ["10K-50K", "Large"],
    8: ["50K-100K", "Large"],
    9: ["100K-500K", "Large"],
    10: ["500K-1M", "Large"],
    11: ["1M-10M", "Very large"],
    12: ["10M-100M", "Very large"],
    13: ["100M-500M", "Very large"],
    14: ["500M-1B", "Very large"],
    15: ["1B+", "Very large"]
}
