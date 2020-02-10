from sharedicom import Clientsharedicom
import random
import os
import psutil
from _thread import *
import time
import statistics
from tcp_latency import measure_latency
pid = 0
import datetime
import pandas as pd

def runClient(ntimes):
    pid = os.getpid()
    client = Clientsharedicom('10.62.9.185', 5001)
    time_file = []
    block_size = []
    # Params:
    # Request dicom images from blockchain network
    for j in range(2):
        for j in range(ntimes):
            #rd = random.randint(1,50)
            rd = 1
            print('Request stated for %i files' % (rd))
            tm, block = client.requestDicom(rd, 'erikson', 'ICMC')
            time_file += tm
            block_size += block
            print('request finish')
    
    tabela = pd.DataFrame()
    tabela.insert(0, "Time", time_file)
    tabela.insert(1, "Block Size (Kb)", block_size)
    tabela.to_csv(os.path.join('../Results/table_sizeblock_%s.csv'%(datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S"))),sep=';')


def mensure(pid):
    
    time.sleep(1)
    server_hostname = '10.62.9.185'

    print("Connecting to {0}".format(server_hostname))

    processTime = []
    iterTime = 0
    latAPIBC = []
    latSocketFile = []
    latPeers = []
    latOderer = []
    latCouchs = []
    
    while psutil.pid_exists(pid):
        print('Read Latency ...')
        peers = []
        couch = []
        processTime.append(iterTime)
        latAPIBC.append(measure_latency(server_hostname, port=3000)[0])
        latSocketFile.append(measure_latency(server_hostname, port=5001)[0])
        latOderer.append(measure_latency(server_hostname, port=7050)[0])
        peers.append(measure_latency(server_hostname, port=7051)[0])
        peers.append(measure_latency(server_hostname, port=8051)[0])
        peers.append(measure_latency(server_hostname, port=9051)[0])
        peers.append(measure_latency(server_hostname, port=10051)[0])
        peers.append(measure_latency(server_hostname, port=11051)[0])
        peers.append(measure_latency(server_hostname, port=12051)[0])
        peers.append(measure_latency(server_hostname, port=13051)[0])
        peers.append(measure_latency(server_hostname, port=14051)[0])
        peers.append(measure_latency(server_hostname, port=15051)[0])
        peers.append(measure_latency(server_hostname, port=16051)[0])
        peers = list(filter(None, peers))
        latPeers.append(statistics.mean(peers))
        couch.append(measure_latency(server_hostname, port=5984)[0])
        couch.append(measure_latency(server_hostname, port=6984)[0])
        couch.append(measure_latency(server_hostname, port=7984)[0])
        couch.append(measure_latency(server_hostname, port=8984)[0])
        couch.append(measure_latency(server_hostname, port=9984)[0])
        couch.append(measure_latency(server_hostname, port=10984)[0])
        couch.append(measure_latency(server_hostname, port=11984)[0])
        couch.append(measure_latency(server_hostname, port=12984)[0])
        couch.append(measure_latency(server_hostname, port=13984)[0])
        couch.append(measure_latency(server_hostname, port=14984)[0])
        couch = list(filter(None, couch))
        latCouchs.append(statistics.mean(couch))
        time.sleep(1)
        iterTime += 1
    

    print('Finished Mensure ...')
    table = pd.DataFrame()
    table.insert(0, "Time", processTime)
    table.insert(1, "Latency Socket", latSocketFile)
    table.insert(2, "Latency API Blockchain", latAPIBC)
    table.insert(3, "Latency Orderer", latOderer)
    table.insert(4, "Latency Peers", latPeers)
    table.insert(5, "Latency Couch", latCouchs)
    table.to_csv('../Results/table_latency_%s.csv'%(datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S")), sep=';')
    


if __name__ == "__main__":
    #start_new_thread(runClient, (1,))
    start_new_thread(mensure, (pid,))
    runClient(1)
