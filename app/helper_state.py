import os
from sklearn.neighbors import NearestNeighbors
from app import util

place = util.Data('state')


def getNearest(table, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(table)
    _, indices = nbrs.kneighbors(table)
    return indices


def get_df(payload, multi=False):
    features = ['Year', 'ID']
    if multi:
        features = features + payload['attribute']
        _df = place.df[place.df['Year'] == payload['year']][features]
        _df = _df.dropna()
        _df = _df.set_index('ID')
    else:
        features.append(payload['attribute'])
        _df = place.df[features]
        _df = _df[(_df['Year'] >= payload['year_range']['start'])
                  & (_df['Year'] <= payload['year_range']['end'])]
    return _df


def sim_places_multi(payload):
    _df = get_df(payload, multi=True)
    indices = getNearest(_df, payload['count']+1)
    id_ = _df.index.tolist().index(payload['id'])

    neighbors = indices[id_]
    return _df.index[neighbors].tolist()[1:]


def sim_places_single(payload):
    _df = get_df(payload)
    pivoted = _df.pivot_table(
        index='ID', columns='Year', values=payload['attribute'])
    pivoted = pivoted.sort_index()
    indices = getNearest(pivoted, payload['count']+1)
    id_ = pivoted.index.tolist().index(payload['id'])
    neighbors = indices[id_]
    return pivoted.index[neighbors].tolist()[1:]


def get_similar_places(payload, multi=False):
    if multi:
        similar_places = sim_places_multi(payload)
    else:
        similar_places = sim_places_single(payload)
    response = []
    for s in similar_places:
        data = {}
        data["place_name"] = place.id_to_name[s][0]
        data["place_id"] = s
        response.append(data)
    return response
