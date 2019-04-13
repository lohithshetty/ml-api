import pandas as pd
import numpy as np
from app import db
import json


with open(db.data_dir + 'supported.json', 'r') as fp:
    supported = json.load(fp)

attr_id_map = pd.read_sql('attr_id_map', db.db_engine)
attr_id_map.set_index("id", drop=True, inplace=True)
attr_id_map = attr_id_map.to_dict(orient="index")

class Data(object):
    def __init__(self, table_name, place_type):
        self.engine = db.db_engine
        self.table_name = table_name
        self.place_type = place_type
        self.supported_attributes = supported[table_name]

    def create_pivoted_table(self):
        print("Creating pivot table for {}".format(self.table_name))
        self.df = pd.read_sql(self.table_name, self.engine)
        values = list(set(self.df.keys())-set(['year', 'id']))
        self.df = None
        pivoted = pd.pivot_table(pd.read_sql(self.table_name, self.engine),
                             index='id',
                             columns='year',
                             values=values)
        keys = list(set([key[0] for key in pivoted.keys()]))
        for i, key in enumerate(keys, 1):
            pivoted[key].iloc[:, 0] = pivoted[key].iloc[:, 0].fillna(0)
            pivoted[key].iloc[:, -1] = pivoted[key].iloc[:, -1].fillna(0)
            print(np.round(i/len(keys), 2), end='\r')
            
        self.df = pivoted.interpolate(axis=1)

        print("Successfully created pivot table for {}".format(self.table_name))
