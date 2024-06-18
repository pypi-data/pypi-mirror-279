import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from datamaker import random_amount, random_double_precision_array, generate_data

# import the user defined sqlalchemy schema
import schema

# User defined data generator functions
custom_providers = {
    "random_amount": random_amount,
    "random_double_precision_array": random_double_precision_array,
}

# define the quantities of data to generate for each table
quantities = {
    "Organization": 1,
    "User": 10,
    "UserOrganization": 10,
    "Project": 20,
    "Client": 10,
}


# create a sql alchemy engine connection to the postgres database
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/capacities"
)

# set the directory where the generated data will be stored
data_dir = Path("./example/generated_data/")

# generate the data according to the schema
# TODO: Consider allowing the user to instantiate a faker instance
data, order = generate_data(
    schema,
    quantities=quantities,
    custom_providers=custom_providers,
    data_dir=data_dir,
)

# get the list of generated data files
files = data_dir.glob("*.csv")

# sort files according to the order of the tables
files = sorted(files, key=lambda x: order.index(x.stem))

# First truncate the existing table
with engine.connect() as conn:
    for file in files:
        table_name = file.stem
        conn.execute(text(f'TRUNCATE "{table_name}" CASCADE;'))

# seed the database with the generated data
for file in files:
    table_name = file.stem
    df = pd.read_csv(file)
    df.to_sql(table_name, engine, if_exists="append", index=False)
