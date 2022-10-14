import zmq

def sub_zmq(port):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from tickdatatable of tickdata database over port {}".format(port))
    socket.connect ("tcp://localhost:%s" %port)

    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        string = socket.recv_string()
        print(string)

if  __name__ == "__main__":
    port = input("Config port for Client to listen for Server, 'Enter' means use defaul port: 5555: ")
    if port:
        port = int(port)
    else:
        port = 5555
    sub_zmq(port)