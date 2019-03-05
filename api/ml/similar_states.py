from api.ml.common_utils import *


def getNearest(table, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(table)
    _, indices = nbrs.kneighbors(table)
    return indices


def get_df(payload, multi=False):
    features = ['Year', 'ID']
    if multi:
        features = features + payload['attribute']
        _df = state_df[state_df['Year'] == payload['year']][features]
        _df = _df.dropna()
        _df = _df.set_index('ID')
    else:
        features.append(payload['attribute'])
        _df = state_df[features]
        _df = _df[(_df['Year'] >= payload['year_range']['start']) & (_df['Year'] <= payload['year_range']['end'])]
    return _df


def sim_states_multi(payload):
    _df = get_df(payload, multi=True)
    indices = getNearest(_df, payload['count']+1)
    id_ = _df.index.tolist().index(payload['id'])

    neighbors = indices[id_]
    return _df.index[neighbors].tolist()[1:]


def sim_states_single(payload):
    _df = get_df(payload)
    pivoted = _df.pivot_table(index='ID', columns='Year', values=payload['attribute'])
    pivoted = pivoted.sort_index()
    indices = getNearest(pivoted, payload['count']+1)
    id_ = pivoted.index.tolist().index(payload['id'])
    neighbors = indices[id_]
    return pivoted.index[neighbors].tolist()[1:]


def get_similar_states(payload, multi=False):
    if multi:
        similar_states = sim_states_multi(payload)
    else:
        similar_states = sim_states_single(payload)
    response = []
    for state in similar_states:
        data = {}
        data["state_name"] = state_id_to_name[state][0]
        data["state_id"] = state
        response.append(data)
    return response
