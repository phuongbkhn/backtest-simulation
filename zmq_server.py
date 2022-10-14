import zmq
import time
from datetime import datetime
from threading import Thread

import psycopg2
from config import config

def read_data_from_db(start_timestamp, end_timestamp,symbols):
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
        if symbols == "all":
            sql_command = "select * from tickdatatable where server_time > {} and server_time < {}".format(start_timestamp,end_timestamp)
        else:
            symbols = tuple(eval(symbols))
            if len(symbols) == 1:
                sql_command = "select * from tickdatatable where server_time > {} and server_time < {} and symbol = '{}'".format(start_timestamp,end_timestamp,symbols[0])
            else:
                sql_command = "select * from tickdatatable where server_time > {} and server_time < {} and symbol in {}".format(start_timestamp,end_timestamp,symbols)
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

def pub_zmq(port,start_time,end_time,speed,symbols):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    data = read_data_from_db(start_time, end_time,symbols)
    for i in range(len(data)):
        symbol = data[i][0]
        event_type = data[i][1]
        price = data[i][4]
        bid = data[i][6]
        ask = data[i][7]
        tick_volume = data[i][5]

        if i < len(data) - 1:
            delta_t = (datetime.fromtimestamp(int(data[i+1][2])/1000000) - datetime.fromtimestamp(int(data[i][2])/1000000)).total_seconds()
        else:
            delta_t = 0

        str_to_send = '"SYMBOL":"{}","EVENT_TYPE":"{}","TIME":{},"PRICE":{},"BID":{},"ASK":{},"TICK_VOLUME":{}'.format(
                            symbol,event_type,now_time(),price,bid,ask,tick_volume)
        print("{" + str_to_send + "}")
        socket.send_string("{" + str_to_send + "}")
    
        time.sleep(delta_t/speed)
    
    print("Done! All data has been sent successfully!")
    socket.send_string("Done! All data has been sent successfully!")
        
def server_zmq():
    port = "1990"

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print("Waiting for something...")
    while True:
    #  Wait for next request from client
        message = socket.recv_string()
        re_mess = message.split("--")
        pub_port = re_mess[0].split(":")[1]
        start_time = re_mess[1].split(":")[1]
        end_time = re_mess[2].split(":")[1]
        speed = float(re_mess[3].split(":")[1])
        symbols = re_mess[4].split(":")[1]
        socket.send_string("Start sending simulation data over port {}".format(pub_port))
        Thread(target=pub_zmq, args=(pub_port,start_time,end_time,speed,symbols,)).start()

if  __name__ == "__main__":
    server_zmq()