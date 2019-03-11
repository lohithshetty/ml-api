import os
from sqlalchemy import create_engine
import pandas as pd
from sklearn.neighbors import NearestNeighbors

engine = create_engine(os.environ['DATABASE_URL'])


def get_state_names(state_ids):
    return [state_id_to_name[i][0] for i in state_ids]


def get_all_attributes(table_name):
    query = 'SELECT * FROM {} FETCH FIRST 5 ROW ONLY'.format(table_name)
    df = pd.read_sql_query(query, con=engine)
    return df.keys().tolist()


def read_table(table_name, attributes):
    return pd.read_sql(table_name, engine, columns=attributes)


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
    for state in similar_states:
        data = {}
        data["state_name"] = state_id_to_name[state][0]
        data["state_id"] = state
        response.append(data)
    return response


features = get_all_attributes('state')
supported_attributes = [x for x in features if "total" in x.lower()]
state_df = read_table('state', supported_attributes)
state_id_to_name = state_df[['ID', 'State']].groupby(
    'ID')['State'].unique().to_dict()
