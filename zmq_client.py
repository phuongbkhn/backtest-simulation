import zmq
import json
import sys

def sub_zmq(port_number):
    port = port_number
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from tickdatatable of tickdata database...")
    socket.connect ("tcp://localhost:%s" % port)

    # Subscribe to symbol
    # symbol = "AVGO US Equity"
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    status = True
    while status == True:
        string = socket.recv_string()
        # print(string)
        if string != "Done! All data has been sent successfully!":
            json_ = json.loads(string)
            print(json_)
        else:
            print("Done! All data has been received successfully!")
            status = False

def client_zmq():
    port = "5558"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://localhost:%s" % port)
    #  Do 10 requests, waiting each time for a response
    for request in range (2):
        print("Sending request ", request,"...")
        socket.send_string("Hello")
        #  Get the reply.
        message = socket.recv()
        print("Received reply: ", request, "[", message, "]")
        sub_zmq(int(port)+1)

if  __name__ == "__main__":
    client_zmq()
