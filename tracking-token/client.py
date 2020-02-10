import pandas as pd
import datetime
from sharedicom import Clientsharedicom
import random
import os
import psutil
from _thread import *
import time
import statistics
from tcp_latency import measure_latency


if __name__ == "__main__":
    print(os.getpid())
    client = Clientsharedicom('10.62.9.185', 5001)
    time_file: list = []
    block_size: list = []
    # Params:
    # Request dicom images from blockchain network
    for j in range(2):
        for j in range(1):
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
    tabela.to_csv(os.path.join('../Results/table_sizeblock_%s.csv' %
                               (datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S"))), sep=';')
