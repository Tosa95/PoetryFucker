def sqlite_row_to_dict(sqlite_row):

    res = {}

    for k in sqlite_row.keys():

        res[k] = sqlite_row[k]

    return res