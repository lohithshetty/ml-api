import pandas as pd
from app import db


class Data(object):
    def __init__(self, table_name):
        self.engine = db.db_engine
        self.table_name = table_name
        self.df = pd.read_sql(self.table_name, self.engine)
        self.df = self.df.dropna()
        self.df = self.df.dropna(axis=1)
        self.features = self.df.keys().tolist()
        self.supported_attributes = [
            x for x in self.features if "total" in x.lower()]
        self.id_to_name = self.df[['ID', 'Name']].groupby(
            'ID')['Name'].unique().to_dict()
