import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('xxx')

import sys
try:
        import psycopg2 as pg
except ImportError:
        print("You should install psycopg2 with the command")
        print("  conda install psycopg2")
        sys.exit(0)
                    
connection_args = {
'host': 'xxx','user': 'postgres',  # username
'password': 'xxx',
'dbname': 'grubhub',  # DB that we are connecting to
'port': xxx  # port we opened on AWS
}

connection = pg.connect(**connection_args)

cursor = connection.cursor()

def topic_info():
    cursor.execute("SELECT km_label, row_number as count_restaurant, price_rating_x as price_rating, max_price, count_top_dishes, dish_topic_keywords, cuisine_topic_keywords FROM complete_inf")

    colname = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall())
    df.columns = colname

    return df
