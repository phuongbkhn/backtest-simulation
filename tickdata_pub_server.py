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

def random_upper_outlier(x):
    return round(x*random.uniform(1.06,1.1),2)

def random_lower_outlier(x):
    return round(x*random.uniform(0.9,0.94),2)

def random_all(x):
    random_list = [0, 'null']
    random_list.append(random_upper_outlier(x))
    random_list.append(random_lower_outlier(x))
    return random.choice(random_list)

def random_5():
    return round(random.uniform(4.9,5.1),2)

def random_500():
    return round(random.uniform(499,501),2)

def now_time():
    return round(datetime.now().timestamp() * 1000000)

def send_data_zmq(start_timestamp, end_timestamp, time_acc=1000):
    port = "5556"
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
        delta_t = data[i][15]

        if symbol == 'FRO US Equity':

            price_5 = random_5()
            bid_5 = random_5()
            ask_5 = random_5()

            str_to_send = '"SYMBOL":"{}","EVEN_TYPE":"{}","TIME":{},"PRICE":{},"BID":{},"ASK":{},"TICK_VOLUME":{}'.format(
                                symbol,event_type,now_time(),price_5,bid_5,ask_5,tick_volume)
            print("{" + str_to_send + "}")
            socket.send_string("{" + str_to_send + "}")

            time.sleep(delta_t/time_acc)
        
        elif symbol == 'AVGO US Equity':
            price_500 = random_500()
            bid_500 = random_500()
            ask_500 = random_500()

            str_to_send = '"SYMBOL":"{}","EVEN_TYPE":"{}","TIME":{},"PRICE":{},"BID":{},"ASK":{},"TICK_VOLUME":{}'.format(
                                symbol,event_type,now_time(),price_500,bid_500,ask_500,tick_volume)
            print("{" + str_to_send + "}")
            socket.send_string("{" + str_to_send + "}")

            time.sleep(delta_t/time_acc)

        else:
            if i % 10 != 0:
                str_to_send = '"SYMBOL":"{}","EVEN_TYPE":"{}","TIME":{},"PRICE":{},"BID":{},"ASK":{},"TICK_VOLUME":{}'.format(
                                    symbol,event_type,now_time(),price,bid,ask,tick_volume)
                print("{" + str_to_send + "}")
                socket.send_string("{" + str_to_send + "}")
            
                time.sleep(delta_t/time_acc)

            else:
                fake_bid = random_all(bid)
                str_to_send = '"SYMBOL":"{}","EVENT_TYPE":"{}","TIME":{},"PRICE":{},"BID":{},"ASK":{},"TICK_VOLUME":{}'.format(
                                    symbol,event_type,now_time(),price,fake_bid,ask,tick_volume)
                print("{" + str_to_send + "}")
                socket.send_string("{" + str_to_send + "}")
                
                time.sleep(delta_t/time_acc)

       
    print("Done! All data has been sent successfully!")

if  __name__ == "__main__":
    e_string = input("Input end time by format: yyyy-m-d-h-m, 'Enter' means input default '2022-1-1-0-0': ")
    if e_string:
        e_year,e_month,e_date,e_hour,e_min = e_string.split("-")
        end_time = to_timestamps(int(e_year),int(e_month),int(e_date),int(e_hour),int(e_min))
    else:
        start_time = to_timestamps(2022,1,1,0,0)

    e_string = input("Input end time by format: yyyy-m-d-h-m (ex: 2022-1-1-0-0), 'Enter' means 'Now': ")
    if e_string:
        e_year,e_month,e_date,e_hour,e_min = e_string.split("-")
        end_time = to_timestamps(int(e_year),int(e_month),int(e_date),int(e_hour),int(e_min))
    else:
        e_time = datetime.now()
        end_time = round(e_time.timestamp() * 1000000)

    send_data_zmq(start_time,end_time)