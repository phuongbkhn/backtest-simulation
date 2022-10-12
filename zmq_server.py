import zmq
import time
from datetime import datetime
import sys


import psycopg2
from config import config

def read_data_from_db(start_timestamp, end_timestamp):
    """ Connect to the PostgreSQL database server and read data """
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
        sql_command = "select * from tickdatatable where server_time > {} and server_time < {}".format(start_timestamp,end_timestamp)
        cur.execute(sql_command)
        data = cur.fetchall()
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed!')


def now_time():
    return round(datetime.now().timestamp() * 1000000)

def pub_zmq(port_number,start_timestamp=0, end_timestamp=now_time(), speed=100):
    port = port_number

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)


    data = read_data_from_db(start_timestamp, end_timestamp)
    for i in range(len(data)):
        symbol = data[i][0]
        event_type = data[i][1]
        price = data[i][4]
        bid = data[i][6]
        ask = data[i][7]
        tick_volume = data[i][5]
        # delta_t = data[i][15]


        str_to_send = '"SYMBOL":"{}","EVEN_TYPE":"{}","TIME":{},"PRICE":{},"BID":{},"ASK":{},"TICK_VOLUME":{}'.format(
                            symbol,event_type,now_time(),price,bid,ask,tick_volume)
        print("{" + str_to_send + "}")
        socket.send_string("{" + str_to_send + "}")
    
        time.sleep(0.05)
    
    print("Done! All data has been sent successfully!")
    socket.send_string("Done! All data has been sent successfully!")
         
def server_zmq():
    port = "5558"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print("Waiting for something...")
    while True:
    #  Wait for next request from client
        message = socket.recv()
        print("Received request: ", message)
        time.sleep (1)  
        socket.send_string("Start sending simulation data")
        pub_zmq(int(port)+1)


if  __name__ == "__main__":
    server_zmq()