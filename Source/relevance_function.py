
# This is the relevance function.
# It's very cowboy, so should only be used on the provided dataset.
def was_correct(query_name, prediction):
    query_name = query_name[:15] if query_name[0] == "c" else query_name[:9]
    prediction = prediction[:-4]
    return query_name == prediction


# # Testing
# query_file_name = "classical.00003-snippet-10-20.wav"
# guess           = "classical.00003.wav"
# print(was_correct(query_file_name, guess))
