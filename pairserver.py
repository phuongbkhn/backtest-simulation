#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

import pandas as pd
import psycopg2
from config import config
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def read_data_from_db():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()

	    # execute a statement
        sql_command = "select * from tickdatatable"
        cur.execute(sql_command)
        data = cur.fetchall()
        print(data)
        return data
      
	# close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# while True:
#  Wait for next request from client
message = socket.recv()
print("Received request: %s" % message)

#  Do some 'work'
# time.sleep(1)

#  Send reply back to client
# socket.send(b"World")

data = read_data_from_db()
for i in range(len(data)):
    send_data = {'symbol':data[i][0], 'price':data[i][4], 'bid':data[i][6], 'ask':data[i][7]}
    send_json = json.dumps(send_data)
    socket.send_string(send_json)
    
    # time.sleep(1)

# if __name__ == '__main__':
#     read_data_from_db()