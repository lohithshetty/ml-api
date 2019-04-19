import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
import app.db_util as util

city = util.Data('city', 2)
city.create_pivoted_table()

county = util.Data('county', 1)
county.create_pivoted_table()

state = util.Data('state', 0)
state.create_pivoted_table()


def get_place(place_type):
    place = None
    if place_type == 0:
        place = state
    elif place_type == 1:
        place = county
    elif place_type == 2:
        place = city
    return place


def getNearest(df1, df2, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(df1)
    return nbrs.kneighbors(df2)


def similar_single_attr_multi_year(pivoted, name_id, attribute, year_range=None, norm_by=None, num=2):
    if norm_by:
        df = pivoted[attribute] / pivoted[norm_by]
    else:
        df = pivoted[attribute]
    df = df.replace([np.inf, -np.inf], np.nan)
    df.iloc[:, 0] = df.iloc[:, 0].fillna(0)
    df.iloc[:, -1] = df.iloc[:, -1].fillna(0)
    df = df.interpolate(axis=1)
    if year_range:
        df = df.loc[:, year_range['start']:year_range['end']]

    distances, indices = getNearest(df, np.asarray(
        df.loc[name_id]).reshape(1, -1), num + 1)
    indices = indices[0]
    similarity_score = (df.loc[name_id].mean() -
                        distances)/df.loc[name_id].mean()

    return df.iloc[indices].index.tolist(), similarity_score[0]


def similar_multi_attr_single_year(pivoted, name_id, attributes, year, norm_by=None, num=2):
    if norm_by:
        df = pivoted[attributes] / pivoted[norm_by]
    else:
        df = pivoted[attributes]
    df = df[[key for key in df.keys() if key[1] == year]]
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
    distances, indices = getNearest(df, np.asarray(
        df.loc[name_id]).reshape(1, -1), num+1)
    indices = indices[0]
    similarity_score = (df.loc[name_id].mean() -
                        distances)/df.loc[name_id].mean()
    return df.iloc[indices].index.tolist(), similarity_score[0]


def get_supported_attributes(place_type):
    place = get_place(place_type)
    response = []
    for _id in place.supported_attributes:
        attribute = {'id': _id}
        attribute.update(util.attr_id_map[_id])
        response.append(attribute)

    return response


def get_common_attributes():
    response = []
    for _id in util.supported['common']:
        attribute = {'id': _id}
        attribute.update(util.attr_id_map[_id])
        response.append(attribute)
    return response


def get_similar_places(payload, multiattr=False):
    place = get_place(payload['place_type'])
    pivoted = place.df
    _id = payload['id']
    norm_by = str(payload['normalize_by'])
    count = payload['count']
    if count > 50:
        count = 50
    try:
        if multiattr:
            attributes = [str(a) for a in payload['attribute']]
            similar_places, score = similar_multi_attr_single_year(pivoted,
                                                                   _id,
                                                                   attributes,
                                                                   payload['year'],
                                                                   norm_by=norm_by,
                                                                   num=count)
        else:
            attribute = str(payload['attribute'])
            similar_places, score = similar_single_attr_multi_year(pivoted,
                                                                   _id,
                                                                   attribute,
                                                                   year_range=payload['year_range'],
                                                                   norm_by=norm_by,
                                                                   num=count)
    except Exception as e:
        print("Exception {}".format(e))
        return []

    response = []
    for place, score in zip(similar_places, score):
        if place == _id:
            continue
        data = {}
        data["place_id"] = place
        data["similarity_score"] = score
        response.append(data)

    return response
