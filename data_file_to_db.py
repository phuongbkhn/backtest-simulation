import pandas as pd
from push_data_to_db import connect_n_push_to_db
from datetime import datetime

# tickdata csv file
tickdatafile = 'tick_data.csv'

def split_info(a):
    split_a = a.split(":")
    return split_a[1].strip()

def make_dataframe(file):
    df = pd.read_csv(file, header=None)

    df['symbol'] = df[0].apply(lambda x: split_info(x))
    df['event'] = df[1].apply(lambda x: split_info(x))
    df['server_time'] = df[2].apply(lambda x: split_info(x))
    df['received_time'] = df[3].apply(lambda x: split_info(x))
    df['price'] = df[4].apply(lambda x: split_info(x))
    df['vol'] = df[5].apply(lambda x: split_info(x))
    df['bid'] = df[6].apply(lambda x: split_info(x))
    df['ask'] = df[7].apply(lambda x: split_info(x))
    df['valid'] = df[8].apply(lambda x: split_info(x))
    df['outliner'] = df[9].apply(lambda x: split_info(x))

    df['server_year'] = df['server_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000000).strftime("%Y"))
    df['server_month'] = df['server_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000000).strftime("%-m"))
    df['server_day'] = df['server_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000000).strftime("%-d"))
    df['server_hour'] = df['server_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000000).strftime("%-H"))
    df['server_minute'] = df['server_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000000).strftime("%-M"))

    df = df.iloc[:,10:]

    return df

if  __name__ == "__main__":
    df = make_dataframe(tickdatafile)
    connect_n_push_to_db(df)
    print("All data in {} is now storing in your database! All tasks done!".format(tickdatafile))