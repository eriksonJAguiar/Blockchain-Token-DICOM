import socket
import pickle
import sys


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
    files = con.recv(4096)
    files = pickle.loads(files)
    print(files)
    #for filename in files: 
        #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        #with open(filename, "wb") as f:
        #    bytes_read = .recv(4096)
        #    if not bytes_read:    
        #        break
            
        #    f.write(bytes_read)
            # update the progress bar
            #progress.update(len(bytes_read))
            # while(f):
            #     con.send(f)
            #     f = fd.read(4096)

        #fd.close()


    print('Sent File ...')
    con.close()
    break