
from relevance_function import *
from get_query_point_list import *
from get_constellation import *
import os
import pickle
from timeit import default_timer as timer
from datetime import datetime

from query import check_song_type_and_increment_correct
from query import check_song_type_and_increment_num_processed


def fingerprintBuilder(db_path, fingerprints, shouldNormalize = True):
    database   = []
    clip_names = []
    for entry in os.scandir(db_path):
        if entry.name[-4:] == '.wav':
            databaseSamples, fs = librosa.load(entry.path)
            if shouldNormalize: databaseSamples     = np.divide(databaseSamples, np.max(databaseSamples)) # Normalize.
            database.append(get_inverted_list(get_constellation(databaseSamples, False)))
            clip_names.append(entry.name)
            print("Completed analysis of file: ", entry.name)
    data = [clip_names, database]
    with open(fingerprints + '/database_file.pickle', 'wb') as f:
        pickle.dump(data, f)

