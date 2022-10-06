# Storing data for backtest

This module read tick data from a csv file, push them to a Postgres database, then use for backtest as simulation by sending tick data one by one.

## Quickly create Postgres database and table

Use file **init.sql** to quickly create database and table for this module.

Run this from terminal:
```
psql -h localhost -U postgres -a -f init.sql
```
*Note*: This works only with Postgres.


## Push data to db

- **database.ini** : information of the local PostgresSQL (host, database name, user, password)
- **config.py** : use information in database.ini to config the connection
- **push_data_to_db.py** : push data from a dataframe to your database.
- *Note*: you need to create a table first, with all columns are matching with columns in the dataframe. Check file *create_table.txt* for prepared sql command.
- **data_file_to_db** : read data from csv file, transform the data, then use push_data_to_db to store them into your db.

Use: after prepare database, and all configurations are done, run this in command line:

```
python3 data_file_to_db.py
```

## tickdata_pub_server.py

- Read data from the database, use Zeromq to make a socket to send data.
- You need to input start and end time to this function.
- The time sleep between 2 sending time is the difference between two time stamps in seconds. You can accelarate this by passing para time_acc in send_data_zmq function (default value: 1000).

Use:
```
python3 tickdata_pub_server.py
```

## tickdata_sub_client.py

- This file to make a client socket, received info from server.
- There is an option to choose symbol, you can edit to what symbol as you interested.

Use:
```
python3 tickdata_sub_client.py
```
## Requirements

You need to have these below packages to run these modules:

- **pandas**
```
pip install pandas
```

- **datetime**
```
pip install DateTime
```

- **tqdm**
```
pip install tqdm
```

- **psycopg2**
```
pip install psycopg2
```

You can also obtain a stand-alone package, not requiring a compiler or external libraries, by installing the psycopg2-binary package from PyPI:
```
pip install psycopg2-binary
```

- **zmq**
```
pip install pyzmq
```
More information about ZeroMQ: https://zeromq.org/
