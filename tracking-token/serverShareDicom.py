import socket
import pickle
import sys
import os


HOST = 'localhost'              
PORT = 5000         
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(5)
print('sevidor iniciado ...')
while True:
    print('We have accepting connections')
    con, cliente = tcp.accept()
    print('Connected by ', cliente)
    filename = con.recv(4096)
    filename = pickle.loads(filename)
    with open(str(filename),"rb") as f:
        #file_ = pickle.dumps(f)
        data = f.read()
        con.send(data)
    # with open(str(filename),"rb") as f:
    #     data=f.read()
    #     con.sendall(data)
    #     con.sendfile()
    
    #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    # f = open(filename, "rb")
    # l = f.read(1024)
    # while(l):
    #     print('Sending ...')
    #     con.send(l)
    #     l = f.read(1024)
    # f.close()
    print('Done!')
    #print(con.recv(4096))


    print('Sent File ...')
    con.close()