from relevance_function import *
from get_query_point_list import *
from get_constellation import *
import os
import pickle
from ranking import *
from timeit import default_timer as timer
from datetime import datetime
num_queries_total = 213

# # Testing
with open('database_file.pickle', 'rb') as f:
    data = pickle.load(f)

clip_names = data[0]
database   = data[1]
num_top_matches_to_show = 10


def analyze_query(entry, shouldNormalize = True):
    print("=============================================================")
    if entry.name[-4:] == '.wav':
        query_name = entry.name
        print("Analyzing", query_name, "...")
        querySamples, fs = librosa.load(entry.path)
        querySamples     = librosa.resample(querySamples, fs, 22050, 'kaiser_fast', True, False)
        if shouldNormalize: querySamples     = np.divide(querySamples, np.max(querySamples)) # Normalization.
        q                = get_constellation(querySamples)
        # Return a list of the query points.
        Q = get_query_point_list(q)

        # Create number of top matches to show.
        best_match = ["void", -1]
        top_N_matches = [["void", -1]]*num_top_matches_to_show

        for k in range(len(database)):
            # Get inverted list of current database entry.
            L = database[k]
            # Lhmn = []
            total = []
            for i in range(len(Q)):
                n = Q[i][0]
                h = Q[i][1]
                # Li = []
                for j in range(len(L[h-1])):
                    # Li.append(L[h-1][j] - n)
                    total.append(L[h-1][j]-n)
                # Lhmn.append(Li)
            # print("L(h)-n:       ", Lhmn)
            values, counts = np.unique(total, return_counts=True)
            if len(counts) > 0:
                ind = np.argmax(counts)
                match_index = values[ind]
                similarity_measure = counts[ind]
                # print(entry.name, "- Match strength:", match_strength)

                lowest_of_index = -1
                for m in range(len(top_N_matches)):
                    lowest_of_index = m if top_N_matches[m][1] < top_N_matches[lowest_of_index][1] else lowest_of_index

                if similarity_measure >= top_N_matches[lowest_of_index][1]:
                    top_N_matches[lowest_of_index] = [clip_names[k], similarity_measure]

                if similarity_measure >= best_match[1]:
                    best_match = [clip_names[k], similarity_measure]

    print("The top", num_top_matches_to_show, "matches are:   [Rank | Clip Name       | Similarity Measure]")

    ranked_top_matches = rank(top_N_matches.copy())
    clip_guessed = ranked_top_matches[0][1]
    correct_bool = was_correct(query_name, clip_guessed)
    hit_was_in_top_N = False
    if correct_bool: hit_was_in_top_N = True
    for i in range(len(ranked_top_matches)):
        if not correct_bool: hit_was_in_top_N = True if was_correct(query_name, ranked_top_matches[i][1]) or hit_was_in_top_N else False
        if was_correct(query_name, ranked_top_matches[i][1]):
            print("                       **", ranked_top_matches[i], "**")
            rank_of_guess = i
        else: print("                         ", ranked_top_matches[i])

    correct_str = "and I was correct :D" if correct_bool else "but I was incorrect :( "
    print("I predicted that the query is:", clip_guessed, correct_str)
    if not correct_bool and hit_was_in_top_N:
        print("I didn't get it right, but it was in the top", num_top_matches_to_show, "...")
    if not correct_bool and not hit_was_in_top_N:
        print("Hit was not in top", num_top_matches_to_show, " :( ")

    # Write to output text file.
    global current_time
    tab = "   "
    with open((str(time_for_output) + 'output.txt'), 'a') as the_file:
        the_file.write(str(query_name) + "   " + tab +
                       str(ranked_top_matches[0][1]) + tab +
                       str(ranked_top_matches[1][1]) + tab +
                       str(ranked_top_matches[2][1]) + '\n')
    return correct_bool


num_classical_processed = 0
num_pop_processed       = 0

num_classical_correct = 0
num_pop_correct       = 0


def check_song_type_and_increment_num_processed(name):
    if name[0] == "p":
        global num_pop_processed
        num_pop_processed += 1
    else:
        global num_classical_processed
        num_classical_processed += 1


def check_song_type_and_increment_correct(name):
    if name[0] == "p":
        global num_pop_correct
        num_pop_correct += 1
    else:
        global num_classical_correct
        num_classical_correct += 1



start = timer()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
time_for_output = now.strftime("%H%M%S")
print("Start Time =", current_time)

for entry in os.scandir("query_recordings"):
    check_song_type_and_increment_num_processed(entry.name)
    query_start_time = timer()
    if analyze_query(entry):
        check_song_type_and_increment_correct(entry.name)
    query_end_time = timer()
    print("Current performance overall:", 100*((num_classical_correct+num_pop_correct)/(num_classical_processed + num_pop_processed)), "% ")
    if num_classical_correct > 0: print("Classical % Correct:", 100 * (num_classical_correct / num_classical_processed), "%")
    if num_pop_correct > 0: print("Pop % Correct:", 100 * (num_pop_correct / num_pop_processed), "%")
    time_remaining = (query_end_time - query_start_time) * (num_queries_total - (num_pop_processed + num_classical_processed))/60
    print("                             Approx time remaining:", round(time_remaining), "minutes.")
end = timer()
print("It has taken ", (end - start)/60, "minutes to process the whole database")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("End Time =", current_time)
