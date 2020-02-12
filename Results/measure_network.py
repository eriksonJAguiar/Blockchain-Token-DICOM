import pandas as pd
import os
import time
import statistics
from tcp_latency import measure_latency
import pandas as pd
import datetime
import psutil
import sys
import contextlib

# processTime = []
# latAPIBC = []
# latSocketFile = []
# latPeers = []
# latOderer = []
# latCouchs = []


@contextlib.contextmanager
def atomic_overwrite(filename):
    temp = filename + '~'
    with open(temp, "w") as f:
        yield f
    # this will only happen if no exception was raised
    os.rename(temp, filename)


if __name__ == "__main__":

    server_hostname = '10.62.9.185'

    print("Connecting to {0}".format(server_hostname))

    #pid = int(sys.argv[1])

    table = pd.DataFrame()
    times = 0

    start = time.time()
    finish = 0
    fname = datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S")
    pid = int(sys.argv[1])
    while psutil.pid_exists(pid) and finish <= 10:
        print('Read Latency ...')
        peers = []
        couch = []
        _processTime = times
        _latAPIBC = measure_latency(server_hostname, port=3000)[0]
        _latSocketFile = measure_latency(server_hostname, port=1021)[0]
        _latOderer = measure_latency(server_hostname, port=7050)[0]
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
        _latPeers = statistics.mean(peers)
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
        _latCouchs = statistics.mean(couch)
        time.sleep(1)
        times += 1
        finish += int((time.time() - start)/3600)

        #print('Finished Mensure ...')
        table = table.append({"Time": _processTime, "LatFTP": _latSocketFile, "LatApi":_latAPIBC, "LatOrder": _latOderer, "LatPeers":_latPeers, "LatCouchs":_latCouchs}, ignore_index=True) # 0, "Time"
        # table.insert() # 1, "Latency Socket"
        # table.insert(_latAPIBC) # 2, "Latency API Blockchain"
        # table.insert(_latOderer) # 3, "Latency Orderer"
        # table.insert(_latPeers) # 4, "Latency Peers"
        # table.insert(_latCouchs) # 5, "Latency Couch"
        table.to_csv('../Results/table_latency.csv', mode='a',sep=';', header=False, index=False)
