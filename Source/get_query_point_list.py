

def get_query_point_list(query_matrix):
    qList = []
    for k in range(len(query_matrix)):
        for n in range(len(query_matrix[k])):
            if query_matrix[k, n]:
                qList.append([n, k + 1])
    return qList