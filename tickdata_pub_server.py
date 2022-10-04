import zmq
import time
from datetime import datetime
import random


import psycopg2
from config import config

def to_timestamps(year,month,day,hour=0,min=0):
    """ convert datetime to timestamp in microseconds """
    dtime = datetime(year,month,day,hour,min)
    dtimestamp = dtime.timestamp() * 1000000
    return round(dtimestamp)

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

# def random_zero_none():
#     fake_errors = [0, None]
#     return random.choice(fake_errors)

def random_outlier(x):
    return round(x*random.uniform(1.06,1.1),2)

def random_all(x):
    random_list = [0, None]
    random_list.append(random_outlier(x))
    return random.choice(random_list)


def send_data_zmq(start_timestamp, end_timestamp, time_acc=1000):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    data = read_data_from_db(start_timestamp, end_timestamp)
    for i in range(len(data)):
        symbol = data[i][0]
        price = data[i][4]
        bid = data[i][6]
        ask = data[i][7]
        delta_t = data[i][15]
        if i % 10 != 0:
            print("%s %.2f %.2f %.2f" %(symbol,price,bid,ask))
            socket.send_string("%s %.2f %.2f %.2f" %(symbol,price,bid,ask))
        
            time.sleep(delta_t/time_acc)
        else:
            fake_price = random_all(price)
            fake_bid = random_all(bid)
            fake_ask = random_all(ask)
            print("{} {} {} {}".format(symbol,fake_price,fake_bid,fake_ask))
            socket.send_string("{} {} {} {}".format(symbol,fake_price,fake_bid,fake_ask))

       
    print("Done! All data has been sent successfully!")

if  __name__ == "__main__":
    s_year,s_month,s_date,s_hour,s_min = input("Input start time by format: yyyy-m-d-h-m (ex: 2022-1-1-0-0): ").split("-")
    start_time = to_timestamps(int(s_year),int(s_month),int(s_date),int(s_hour),int(s_min))

    e_string = input("Input end time by format: yyyy-m-d-h-m (ex: 2022-1-2-0-0), 'Enter' means 'Now': ")
    if e_string:
        e_year,e_month,e_date,e_hour,e_min = e_string.split("-")
        end_time = to_timestamps(int(e_year),int(e_month),int(e_date),int(e_hour),int(e_min))
    else:
        e_time = datetime.now()
        end_time = round(e_time.timestamp() * 1000000)

    send_data_zmq(start_time,end_time)