import pandas as pd
import numpy as np
from app import db


class Data(object):
    def __init__(self, table_name):
        self.engine = db.db_engine
        self.table_name = table_name
        self.df = pd.read_sql(self.table_name, self.engine)
        self.supported_attributes = ["Total_Revenue","Total_Taxes"]
        self.id_to_name = {'10':'temp'}
        
    def create_pivoted_table(self):
        print("Creating pivot table for {}".format(self.table_name))
        self.df = pd.pivot_table(self.df, index='id',columns='year', values=list(set(self.df.keys())-set(['year', 'id'])))
        keys = list(set([key[0] for key in self.df.keys()]))
        for i, key in enumerate(keys, 1):
            self.df[key].iloc[:, 0] = self.df[key].iloc[:, 0].fillna(0)
            self.df[key].iloc[:, -1] = self.df[key].iloc[:, -1].fillna(0)
            self.df[key] = self.df[key].interpolate(axis=1)
        print(np.round(i/len(keys), 2), end='\r')

        print(' DONE !')


# '''

# DB:
#    state
#    county
#    city
#    supported_attr
#    attr_id_map
   
# '''