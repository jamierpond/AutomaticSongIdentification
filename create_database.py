
import os
import librosa.display
import pickle
from get_constellation import *

db_path =    "database_recordings"
output_file = "database_file.pickle"

def create_database(shouldNormalize = True):
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
    with open(output_file, 'wb') as f:
        pickle.dump(data, f)


create_database()

# Testing
with open(output_file, 'rb') as f:
    database = pickle.load(f)
print(len(database[0][0]))
print(database[1][0])
