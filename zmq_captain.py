import zmq
from datetime import datetime

symbols = ["CNE LN Equity","TLW LN Equity"]

def to_timestamps(year,month,day,hour=0,min=0):
    """ convert datetime to timestamp in microseconds """
    dtime = datetime(year,month,day,hour,min)
    dtimestamp = dtime.timestamp() * 1000000
    return round(dtimestamp)

def client_zmq(pub_sub_port,start_time,end_time,speed,symbols):
    port = "1990"

    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:%s" % port)
    
    if symbols:
        sending_mess = '"port":{}--"start_time":{}--"end_time":{}--"speed":{}--"symbols":{}'.format(pub_sub_port,start_time,end_time,speed,symbols)
    else:
        sending_mess = '"port":{}--"start_time":{}--"end_time":{}--"speed":{}--"symbols":"all"'.format(pub_sub_port,start_time,end_time,speed)
    print("Sending request: {}".format(sending_mess))
    socket.send_string(sending_mess)

    #  Get the reply.
    message = socket.recv_string()
    print("Received reply: ", message)

if  __name__ == "__main__":
    pub_sub_port = input("Config port to Server & Client, 'Enter' means use defaul port: 5555: ")
    if pub_sub_port:
        pub_sub_port = int(pub_sub_port)
    else:
        pub_sub_port = 5555

    s_string = input("Input start time by format: yyyy-m-d-h-m, 'Enter' means input default '2022-1-1-0-0': ")
    if s_string:
        s_year,s_month,s_date,s_hour,s_min = s_string.split("-")
        start_time = to_timestamps(int(s_year),int(s_month),int(s_date),int(s_hour),int(s_min))
    else:
        start_time = to_timestamps(2022,1,1,0,0)

    e_string = input("Input end time by format: yyyy-m-d-h-m (ex: 2022-1-1-0-0), 'Enter' means 'Now': ")
    if e_string:
        e_year,e_month,e_date,e_hour,e_min = e_string.split("-")
        end_time = to_timestamps(int(e_year),int(e_month),int(e_date),int(e_hour),int(e_min))
    else:
        e_time = datetime.now()
        end_time = round(e_time.timestamp() * 1000000)

    speed = input("Input speed of simulation progress, 'Enter' means normal speed: ")
    if speed:
        speed = float(speed)
    else:
        speed = 1

    client_zmq(pub_sub_port,start_time,end_time,speed,symbols)