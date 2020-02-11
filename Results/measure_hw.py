import pandas as pd
import os
import time
import statistics
from tcp_latency import measure_latency
import pandas as pd
import datetime
import psutil
import sys
from _thread import *


processTime: list = []
times = 0
processCpu: list = []
processMem: list = []

def mensure_cpu(pids):
    cpus = []
    for pid in pids:
        p = psutil.Process(pid)
        cpu = p.cpu_percent(interval=5)
        cpus.append(cpu)
    
    return statistics.mean(cpus)

def mensure_mem(pids):
    mem = []
    for pid in pids:
        p = psutil.Process(pid)
        m = p.memory_percent()
        mem.append(m)

    
    time.sleep(5)

    return statistics.mean(mem)

def get_pids(ports):
    pids = []
    pcss = psutil.psutil.net_connections()
    for p in pcss:
        if p.laddr[1] in ports:
            pids.append(p.laddr[1])

    return pids
    

if __name__ == "__main__":
    
    ports = [7050, 5001, 3000, 7051, 11051, 1026]

    
    pid = int(sys.argv[1])

    pids = get_pids(ports)
    

    while psutil.pid_exists(pid):
        processTime.append(times)
        processCpu.append(mensure_cpu(pids))
        m = start_new_thread(mensure_mem, (pids,))
        processMem.append(m)
        time.sleep(1)
        times += 1

    print('Finished Mensure ...')
    table = pd.DataFrame()
    table.insert(0, "Time", processTime)
    table.insert(1, "Usage CPU", processCpu)
    table.insert(2, "Usage Memory", processMem)
    table.to_csv('../Results/table_hw_%s.csv' %(datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S")), sep=';')


    
