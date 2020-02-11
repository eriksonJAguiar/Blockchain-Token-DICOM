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
    time_file: list = []
    block_size: list = []
    # Params:
    # Request dicom images from blockchain network
    for j in range(30):
        for i in range(10):
            rd = i*2
            client = Clientsharedicom('10.62.9.185', 5001)
            print('Request stated for %i files' % (rd))
            client.requestDicom(rd, 'erikson', 'ICMC')
            print('request finish')

    # tabela = pd.DataFrame()
    # tabela.insert(0, "Time", time_file)
    # tabela.insert(1, "Block Size (Kb)", block_size)
    # tabela.to_csv(os.path.join('../Results/table_sizeblock_%s.csv' %
    #                            (datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S"))), sep=';')
