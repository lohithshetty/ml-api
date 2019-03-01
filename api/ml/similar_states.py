from api.ml.common_utils import *


def getNearest(table, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(table)
    _, indices = nbrs.kneighbors(table)
    return indices


def get_df(data, df):
    features = ['Year', 'ID'] + [data['attribute']]
    _df = df[features]
    return _df[(_df['Year'] >= data['years']['start']) & (_df['Year'] <= data['years']['end'])]


def get_similar_states(data):
    _df = get_df(data, state_df)
    pivoted = _df.pivot_table(index='ID', columns='Year', values=data['attribute'])
    pivoted = pivoted.sort_index()
    indices = getNearest(pivoted, data['count']+1)
    id_ = pivoted.index.tolist().index(data['id'])

    neighbors = indices[id_]
    similar_states = pivoted.index[neighbors].tolist()[1:]
    response = []
    for state in similar_states:
        data = {}
        data["attribute_name"] = state_id_name_map[state][0]
        data["state_id"] = state
        response.append(data)
    return response
