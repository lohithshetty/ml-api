import pandas as pd
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import psycopg2
import io
import pandas as pd
import psycopg2
import config
import settings

# TODO: Read from config file
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def get_all_attributes(table_name):
    query = 'SELECT * FROM {} FETCH FIRST 5 ROW ONLY'.format(table_name)
    df = pd.read_sql_query(query, con=engine)
    return df.keys().tolist()


def load_data(table_name, attributes):
    return pd.read_sql(table_name, engine, columns=attributes)


def get_state_names(state_ids):
    return [state_id_name_map[i][0] for i in state_ids]


ATTRIBUTES = get_all_attributes('states_data')
supported_attributes = [i for i in ATTRIBUTES if "total" in i.lower()]
common_attributes = ['Year', 'ID', 'State']
state_df = load_data('states_data', supported_attributes + common_attributes)
state_id_name_map = state_df[['ID', 'State']].groupby('ID')['State'].unique().to_dict()
