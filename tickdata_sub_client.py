import zmq

port = "5556"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from tickdatatable of tickdata database...")
socket.connect ("tcp://localhost:%s" % port)

# Subscribe to symbol
symbol = "CNE LN Equity"
socket.setsockopt_string(zmq.SUBSCRIBE, symbol)

while True:
    string = socket.recv()
    print(string)