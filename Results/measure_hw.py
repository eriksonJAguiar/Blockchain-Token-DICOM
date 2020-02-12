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
import contextlib

# processTime: list = []
# processCpu: list = []
# processMem: list = []

@contextlib.contextmanager
def atomic_overwrite(filename):
    temp = filename + '~'
    with open(temp, "w") as f:
        yield f
    os.rename(temp, filename) # this will only happen if no exception was raised

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
    pcss = psutil.net_connections()
    for p in pcss:
        if p.laddr[1] in ports:
            pids.append(p.pid)

    return pids
    

if __name__ == "__main__":
    
    ports = [7050, 5001, 3000, 7051, 11051, 1026]

    
    pid = int(sys.argv[1])

    print('Get pids')
    pids = get_pids(ports)
    
    start = time.time()
    finish = 0
    table = pd.DataFrame()

    times = 0
    print('Started collect')
    while psutil.pid_exists(pid) and finish <= 10:
        processTime = times
        processCpu = mensure_cpu(pids)
        processMem = start_new_thread(mensure_mem, (pids,))
        times += 1
        finish += int((time.time() - start)/3600)
        time.sleep(1)
        print("Mem: {0}, CPU: {1}".format(processCpu, processMem))
        #print('Finished Mensure ...')
        table = table.append({"Time":  processTime, "UsageCPU": processCpu, "UsageMem": processMem})
        # table.insert(0, "Time", processTime)
        # table.insert(1, "Usage CPU", processCpu)
        # table.insert(2, "Usage Memory", processMem)
        table.to_csv('../Results/table_hw.csv', sep=';', header=False, index=False)


    
