import nwalign as nw
import pydicom
import glob

def getHash(path):
    result = glob.glob(os.path.join(path_, "*.dcm"))
    hs = []
    for res in result:
        image = pydicom.dcmread(str(res))
        h = str(image[0x08, 0x17].value)
        hs.append(h)
    
    return hs


def calcAlign(hashes):
    scores = []
    for hs in hashes:
        for h in hashes:
            s = nw.score_alignment(hs,h)
            scores.append(s)
    

    return scores
            
if __name__ == "__main__":
    hs = getHash('/media/erjulioaguiar/F30E-2F6C/SharedDicom/')
    s = calcAlign(hs)
    print(s)