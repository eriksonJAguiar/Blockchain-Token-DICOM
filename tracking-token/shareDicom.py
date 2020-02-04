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
#file = pydicom.read_file("../../DICOM_TCIA/CPTAC-CM/C3L-00275/12-06-1999-XR\ CHEST\ 1V\ PORTABLE-53067/1-AP-73378/000000.dcm")
#image = pydicom.dcmread(file)

#print(image)

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
        pathzip.append(path_)
        result = list(Path(path_).rglob("*.dcm"))
        image = pydicom.dcmread(str(result[0]))

        dicomId = image.data_element('PatientID').value
        t = str(datetime.datetime.now().timestamp())
        value = str(dicomId)+t
        sha =  hashlib.sha256()
        sha.update(value.encode('utf-8'))
        token = sha.hexdigest()
        
        zipname = '%s.zip'%(token)
        zf = zipfile.ZipFile(os.path.join(path_,zipname), "w")
        
        for res in result:
            image = pydicom.dcmread(str(res))
            new_tag = ((0x08,0x17))
            image.add_new(new_tag,'CS',token) 
            image.save_as(str(res))
            zf.write(str(res))
        
        pathzip.append(zipname)
        zf.close()
    
    return zipname

    





def shareDicom():
    paths = readPathDicom("../../DICOM_TCIA/")
    sharefiles = readDicom(paths,1)
    print(sharefiles)


shareDicom()

#file = pydicom.read_file(result[0])
#image = pydicom.dcmread(str(result[0]))

#print(image)