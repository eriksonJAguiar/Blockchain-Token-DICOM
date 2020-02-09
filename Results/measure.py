import psutil
import pandas as pd
import os
import time
import statistics
import iperf3


if __name__ == "__main__":
    iperf3.Client()
     
    client = iperf3.Client()
    client.duration = 60
    client.server_hostname = '10.62.9.185'
    client.port = 3000
    client.protocol = 'udp'


    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
    else:
        print('')
        print('Test completed:')
        print('  started at         {0}'.format(result.time))
        print('  bytes transmitted  {0}'.format(result.bytes))
        print('  jitter (ms)        {0}'.format(result.jitter_ms))
        print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

        print('Average transmitted data in all sorts of networky formats:')
        print('  Kilobits per second  (kbps)  {0}'.format(result.kbps))