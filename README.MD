# BACKTEST SIMULATION

This module is used to simulated a trading system for backtest with historical tick data, includes:
- Read tick data from a csv file.
- Push them to a Postgres database.
- Then replay the data for stock/crypto trading for backtest.

I use PostgreSQL to build a database, a small dataset from stock market for this simulation.

In case you need, download from this link: [tick data](https://drive.google.com/drive/folders/16RFYeoyEFoMrB_yBCC1AX6HnnF6Kiy0s?usp=sharing)

## Quickly create Postgres database and table

Use file **init.sql** to quickly create database and table for this module.

Run this from terminal:
```
psql -h localhost -U postgres -a -f init.sql
```
*Note, again*: This works only with Postgres.


## Push data to db

- **database.ini** : information of the local PostgresSQL (host, database name, user, password)
- **config.py** : use information in database.ini to config the connection
- **file_to_db.py** : read data from csv file, transform the data, then use push_data_to_db to store them into your db.

- *Note*: you need to create a table first, with all columns are matching with columns in the dataframe. Check file *create_table.txt* for prepared sql command.


Use: after prepare database, and all configurations are done, run this in command line:

```
python3 data_file_to_db.py
```

## zmq_server.py

- Read data from the database, use Zeromq to make a socket to send data.

Use:
```
python3 zmq_server.py
```

## zmq_client.py

- This file to make a client socket, received info from server.

Use:
```
python3 zmq_client.py
```

When run this, you should to pass a socket port to received wanted data, default port: 5555

## zmq_captain.py

- This file to make a request to zmq_server to start the simulation.

Use:
```
python3 zmq_client.py
```

When run this, you should to pass
- Start time: start point of the simulation, default is starting of 2022.
- End time: end point of the simulation, default is until now.
- Port number: a socket port for the server to send data through, default port: 5555
- Speed of simulation: in case you want to accurate the simulation, use this parameter. Simulation speed = Real speed / speed.

## How to run:
- Start zmq_server to listen signal from captain.
- Start zmq_client to ready to receive data.
- Start Captain to make the request.


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


Author: @phuongbkhn

LinkedIn: https://www.linkedin.com/in/phuongphanvien/
