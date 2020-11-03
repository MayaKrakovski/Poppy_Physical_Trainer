import socket
import json

#TODO DELETE THIS FILE

#server recive info
if __name__=='__main__':
    print('Hello Server')

    # create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Bind the socket to a speicific port
    server_address = ('localhost',8888)
    sock.bind(server_address)

    while True:
        print('Waiting for data...')
        data , address = sock.recvfrom(4096) #not more than 4096 bytes
        print ('received {} bytes from {}'.format(len(data), address))
        #data = json.loads(data)
        print(data)
