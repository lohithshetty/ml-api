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
df = pd.read_sql_query('select * from states_data', con=engine)

# Find a better way to do this ?
state_id_name_map = df[['ID', 'State']].groupby('ID')['State'].unique().to_dict()
years = df['Year'].unique().tolist()


def get_state_names(state_ids):
    return [state_id_name_map[i][0] for i in state_ids]


def plot_similar_states(state, similar_states, attribute):
    fig, ax = plt.subplots(figsize=(20, 10))
    for _id in similar_states:
        ax.plot(years, df[df['ID'] == _id][attribute])
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    ax.set_facecolor((.153, 0.153, 0.153))
    ax.grid(True)
    plt.legend(get_state_names(similar_states))
    plt.xlabel('Year')
    plt.ylabel(attribute)
    fig_name = "./plots/{}_{}.png".format(state, attribute.lower())
    # fig.savefig(fig_name)