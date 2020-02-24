from hexhamming import hamming_distance
import pydicom
import os
from pathlib import Path
import pandas as pd
from Levenshtein import distance
import text_align as align
import math
from collections import Counter

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
    f = open('sim.txt',mode='w',encoding='utf-8')
    for hs in hashes:
        for h in hashes:
            s = hamming_distance(hs,h)
            f.write(str(s) + os.linesep)

    f.close()
            

def calcSimLev(hashes):
    scores = []
    f = open('sim_lev.txt',mode='w',encoding='utf-8')
    for hs in hashes:
        for h in hashes:
            s = distance(hs,h)
            f.write(str(s) + os.linesep)

    f.close()


def calcAlign(hashes):
    scores = []
    f = open('sim_align.txt',mode='w',encoding='utf-8')
    for hs in hashes:
        for h in hashes:
            s = align.calculate_redundancy(hs,h)
            f.write(str(s) + os.linesep)

    f.close()

def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

def calcEntropy(hashes):
    scores = []
    f = open('entropy.txt',mode='w',encoding='utf-8')
    for hs in hashes:
        for h in hashes:
            s = entropy(h)
            f.write(str(s) + os.linesep)

            
if __name__ == "__main__":
    hs = getHash('/media/erjulioaguiar/F30E-2F6C/SharedDicom/')
    calcEntropy(hs)
    
