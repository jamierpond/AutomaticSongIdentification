

from inverted_list import *
from get_query_point_list import *


# Database Example
db = np.array([[0, 0, 0, 1, 1, 0, 0],
               [1, 0, 0, 1, 0, 1, 0],
               [0, 0, 1, 0, 1, 0, 0],
               [1, 1, 0, 1, 0, 1, 0]])

# Query
q = np.array([[0, 1, 1],
              [0, 1, 0],
              [1, 0, 1],
              [0, 0, 0]])


# This is to get them the right way around.
# Basically ignore this.
q  = np.flip(q, axis=0)
db = np.flip(db, axis=0)

# Get the inverted list of the database entry.
db_fingerprint    = get_inverted_list(db)

# Return a list of the query points.
Q = get_query_point_list(q)
print("Query (n, h): ", Q)

L = db_fingerprint
Lhmn = []
total = []
for i in range(len(Q)):
    n = Q[i][0]
    h = Q[i][1]
    Li = []
    for j in range(len(L[h-1])):
        Li.append(L[h-1][j] - n)
        total.append(L[h-1][j]-n)
    Lhmn.append(Li)
print("L(h)-n:       ", Lhmn)

values, counts = np.unique(total, return_counts=True)
ind = np.argmax(counts)
match_index = values[ind]
match_strength = counts[ind]
print("Index of match:", match_index)
print("Strength of match:", match_strength)

