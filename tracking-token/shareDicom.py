import pydicom
import random
from pydicom.datadict import tag_for_keyword
from pydicom.tag import Tag
from pathlib import Path
from shutil import make_archive
from pydicom.datadict import DicomDictionary, keyword_dict
import hashlib
import datetime
import zipfile
import os
import requests
import socket
import pickle
#file = pydicom.read_file("../../DICOM_TCIA/CPTAC-CM/C3L-00275/12-06-1999-XR\ CHEST\ 1V\ PORTABLE-53067/1-AP-73378/000000.dcm")
#image = pydicom.dcmread(file)

#print(image)

HOST = 'localhost'     
PORT = 5000            


def readPathDicom(path):

    result = list(Path(path).rglob("*.dcm"))

    dir = str(result[0]).split('/')
    dir = dir[len(dir)-2]
    dirs = []
    for r in result:
        d = str(r).split('/')
        if not (d[len(d)-2]) == dir:
            res = Path(str(r)).parent.absolute()
            dirs.append(str(res))
            dir = str(r).split('/')
            dir = dir[len(dir)-2]

    return dirs


def readDicom(paths, amount):
    pathzip = []
    if (amount > len(paths)):
       return
    for i in range(amount):
        rd = random.randint(0,amount)
        path_ = paths[rd]
        result = list(Path(path_).rglob("*.dcm"))
        image = pydicom.dcmread(str(result[0]))

        dicomId = image.data_element('PatientID').value
        t = str(datetime.datetime.now().timestamp())
        value = str(dicomId)+t
        sha =  hashlib.sha256()
        sha.update(value.encode('utf-8'))
        token = sha.hexdigest()
        
        zipname = '%s.zip'%(token)
        zf = zipfile.ZipFile(os.path.join('~/SharedDicom',zipname), "w")
        
        for res in result:
            print(res)
            break
            image = pydicom.dcmread(str(res))
            new_tag = ((0x08,0x17))
            image.add_new(new_tag,'CS',token) 
            image.save_as(str(res))
            zf.write(str(res))
        
        zf.close()
        pathzip.append(os.path.join('~/SharedDicom',zipname))
        
    
    return pathzip

#req.body.dicomId, req.body.typeExam, req.body.owner
def readAllDicom(paths,owner,examType):
    files = []
    for path_ in paths:
        try:
            req = dict()
            result = list(Path(path_).rglob("*.dcm"))
            image = pydicom.dcmread(str(result[0]))

            dicomId = image.data_element('AccessionNumber').value

            req['dicomId'] = dicomId
            req['typeExam'] = examType
            req['owner'] = owner
            
            requests.post('http://10.62.9.185:3000/api/createDicom',json=req)
        except:
            print('%s File not register'%(dicomId))
            continue

    print('Regiter Successful')
    


def shareDicom(amount):
    paths = readPathDicom("../../DICOM_TCIA/")
    print(paths)
    #
    # sharefiles = readDicom(paths,amount)
    
    # tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # tcp.connect((HOST, PORT))

    # data_send = pickle.dumps(sharefiles)
    # tcp.send(data_send)
    # data = tcp.recv(4096)
    # print(pickle.loads(data))
    # tcp.close()
    

def registerDicom(hprovider, examType):
    paths = readPathDicom("../../DICOM_TCIA/")
    regs = readAllDicom(paths,hprovider,examType)


registerDicom('erikson','Digital Raio-X')

#shareDicom(1)

#registerDicom('erikson','Digital Raio-X')

#file = pydicom.read_file(result[0])
#image = pydicom.dcmread(str(result[0]))

#print(image)