import socket
import pickle
import sys
import os
from _thread import *
import threading
import time

HOST = 'localhost'              
PORT = 5000         
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(5)


def server_socket(con):
    filename = con.recv(1024)
    filename = pickle.loads(filename)
    time.sleep(100)
    with open(str(filename),"rb") as f:
        data = f.read(1024)
        print('Sending ...')
        while(data):
            con.send(data)
            data = f.read(1024)

    print('Done!')


    print('Sent File ...')
    con.close()

def main():
    while True:
        print('sevidor iniciado ...')
        print('We have accepting connections')
        con, cliente = tcp.accept()
        print('Connected by ', cliente)
        start_new_thread(server_socket,(con,)) 
    
    tcp.close()


if __name__ == "__main__":
    main()