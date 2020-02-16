from hexhamming import hamming_distance
import pydicom
import os
from pathlib import Path
import pandas as pd

def getHash(path):
    #result = glob.glob(os.path.join(path, "*.dcm"))
    result =  Path('/media/erjulioaguiar/F30E-2F6C/SharedDicom/').rglob('*.dcm')
    hs = set()
    for res in result:
       image = pydicom.dcmread(str(res))
       h = str(image[0x08,0x17].value)
       hs.add(h)
    
    return list(hs)



def calcSim(hashes):
    scores = []
    f = open('sim.txt','w')
    for hs in hashes:
        for h in hashes:
            s = hamming_distance(hs,h)
            f.write(str(s)+"/n")

    f.close()
            
    
            
if __name__ == "__main__":
    hs = getHash('/media/erjulioaguiar/F30E-2F6C/SharedDicom/')
    calcSim(hs)
    