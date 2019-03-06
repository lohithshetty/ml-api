import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine
import pandas as pd
import settings


# TODO: Read from config file
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def get_all_attributes(table_name):
    query = 'SELECT * FROM {} FETCH FIRST 5 ROW ONLY'.format(table_name)
    df = pd.read_sql_query(query, con=engine)
    return df.keys().tolist()


def read_table(table_name, attributes):
    return pd.read_sql(table_name, engine, columns=attributes)


def get_state_names(state_ids):
    return [state_id_to_name[i][0] for i in state_ids]


supported_attributes = get_all_attributes('state')
common_attributes = ['Year', 'ID', 'State']
state_df = read_table('state', supported_attributes)
state_id_to_name = state_df[['ID', 'State']].groupby('ID')['State'].unique().to_dict()
# Fix this
# state_name_to_id = dict(reversed(item) for item in state_id_to_name.items())
