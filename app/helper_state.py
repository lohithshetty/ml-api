import os
from sqlalchemy import create_engine
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from app import db


class State(object):
    def __init__(self, table_name):
        self.engine = db.db_engine
        self.table_name = table_name
        self.df = pd.read_sql(self.table_name, self.engine)
        self.features = self.df.keys().tolist()
        self.supported_attributes = [
            x for x in self.features if "total" in x.lower()]
        self.state_id_to_name = self.df[['ID', 'State']].groupby(
            'ID')['State'].unique().to_dict()

    def get_state_names(self, state_ids):
        return [self.state_id_to_name[i][0] for i in state_ids]


state = State('state')


def getNearest(table, num):
    nbrs = NearestNeighbors(n_neighbors=num, algorithm='auto').fit(table)
    _, indices = nbrs.kneighbors(table)
    return indices


def get_df(payload, multi=False):
    features = ['Year', 'ID']
    if multi:
        features = features + payload['attribute']
        _df = state.df[state.df['Year'] == payload['year']][features]
        _df = _df.dropna()
        _df = _df.set_index('ID')
    else:
        features.append(payload['attribute'])
        _df = state.df[features]
        _df = _df[(_df['Year'] >= payload['year_range']['start'])
                  & (_df['Year'] <= payload['year_range']['end'])]
    return _df


def sim_states_multi(payload):
    _df = get_df(payload, multi=True)
    indices = getNearest(_df, payload['count']+1)
    id_ = _df.index.tolist().index(payload['id'])

    neighbors = indices[id_]
    return _df.index[neighbors].tolist()[1:]


def sim_states_single(payload):
    _df = get_df(payload)
    pivoted = _df.pivot_table(
        index='ID', columns='Year', values=payload['attribute'])
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
    for s in similar_states:
        data = {}
        data["state_name"] = state.state_id_to_name[s][0]
        data["state_id"] = s
        response.append(data)
    return response
