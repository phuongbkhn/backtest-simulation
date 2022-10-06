import zmq
import json

port = "5556"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from tickdatatable of tickdata database...")
socket.connect ("tcp://localhost:%s" % port)

# Subscribe to symbol
# symbol = "AVGO US Equity"
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    string = socket.recv_string()
    print(string)

    json_ = json.loads(string)
    print(json_)