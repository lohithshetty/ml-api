from sqlalchemy import create_engine
import os
import io
import pandas as pd
import argparse


print("Creating PSQL engine to {}".format(os.environ['DATABASE_URL']))
db_engine = create_engine(os.environ['DATABASE_URL'])
data_dir = "app/data/"
data_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]


def init_db(data_dir):
    for csv in data_files:
        create_table(data_dir + '/' + csv, csv.split('.')[0])


def create_table(csv, table_name):
    print("Creating table {} from file {}".format(table_name, csv))
    df = pd.read_csv(csv)
    df = df.dropna(axis=1)
    df.head(0).to_sql(table_name, db_engine, if_exists='replace',
                      index=False)  # truncates the table
    conn = db_engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    cur.copy_from(output, table_name, null="")  # null values become ''
    conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process datapath')
    parser.add_argument('-p', '--path', required=True,
                        help='path of the original data(csv) files')
    args = parser.parse_args()

    init_db(args.path)
