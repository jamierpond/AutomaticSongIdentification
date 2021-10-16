
# Returns an inverted list of a given binary matrix.

import numpy as np


def get_inverted_list(binary_matrix):
    num_frequency_bins, num_timestamps = np.shape(binary_matrix)
    # print("Num freq bins: ", num_frequency_bins, "Num timestamps: ", num_timestamps)
    inverted_list = []
    for k in range(num_frequency_bins):
        sub_list = []
        for n in range(num_timestamps):
            if binary_matrix[k, n]:
                sub_list.append(n)
        inverted_list.append(sub_list)
    return inverted_list

# # Testing
# bm = np.array([[0, 1, 0, 1],
#                [0, 0, 0, 0],
#                [0, 1, 0, 0]])
# print(get_inverted_list(bm))
#
#
# q = np.array([[1],
#               [0],
#               [1]])

# Should print [[1, 3], [], [1]]
# Which does seem right.

