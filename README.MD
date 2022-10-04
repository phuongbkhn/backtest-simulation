# Storing data for backtest

This module read tick data from a csv file, push them to a Postgres database, then use for backtest as simulation by sending tick data one by one.

## Push data to db

- **database.ini** : information of the local PostgresSQL (host, database name, user, password)
- **config.py** : use information in database.ini to config the connection
- **push_data_to_db.py** : push data from a dataframe to your database.
- *Note*: you need to create a table first, with all columns are matching with columns in the dataframe.
- **data_file_to_db** : read data from csv file, transform the data, then use push_data_to_db to store them into your db.

Use: after prepare database, and all configurations are done, run this in command line:

```
python3 data_file_to_db.py
```

## tickdata_pub_server.py

- Read data from the database, use Zeromq to make a socket to send data.
- You need to input start and end time to this function.
- The time sleep between 2 sending time is the difference between two time stamps in seconds.

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
