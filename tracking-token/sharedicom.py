import socket
import pickle
import sys
import os
import threading
import time
import pydicom
import random
import hashlib
import datetime
import zipfile
import requests
from pydicom.datadict import tag_for_keyword
from pydicom.tag import Tag
from pathlib import Path
from shutil import make_archive
from pydicom.datadict import DicomDictionary, keyword_dict
from _thread import *


class  Serversharedicom:

    def __init__(self,path,IP,PORT):
        self.path = path
        self.HOST = IP             
        self.PORT = PORT        
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen(5)

    def __readPathDicom(self,path):

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


    def __readAllDicom(self,paths,owner,examType):
        files = []
        for path_ in paths:
            try:
                req = dict()
                result = list(Path(path_).rglob("*.dcm"))
                image = pydicom.dcmread(str(result[0]))
            
                dicomId = image.data_element('SOPInstanceUID').value

                req['dicomId'] = dicomId
                req['typeExam'] = examType
                req['owner'] = owner
                
                requests.post('http://%s:3000/api/createDicom'%(self.HOST),json=req)
            except:
                print('%s File not register'%(dicomId))
                continue

        print('Regiter Successful')


    def __readDicom(self,paths, amount):
        pathzip = []
        tokens = []
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
            zf = zipfile.ZipFile(os.path.join(path_,zipname), "w")
            
            for res in result:
                image = pydicom.dcmread(str(res))
                new_tag = ((0x08,0x17))
                image.add_new(new_tag,'CS',token) 
                image.save_as(str(res))
                zf.write(str(res))
            
            zf.close()
            pathzip.append(os.path.join(path_,zipname))
            tokens.append(token)
            
        
        return pathzip,token

    #req.body.tokenDicom, req.body.to, req.body.toOrganization
    def __server_socket(self,con):
        while True:
            amount = pickle.loads(con.recv(1024))
            if amount:
                break
            print('Amount: %i'%(amount))
            user = con.recv(4096)
            user = pickle.loads(user)
            org = con.recv(4096)
            org = pickle.loads(org)
            print('identities: %s and %s'%(user,org))
            paths = self.__readPathDicom(self.path)
            sharefiles,tokens = self.__readDicom(paths,amount)
            for filename, token in zip(sharefiles,tokens):
                log = dict()
                fname = filename.split('/')
                fname = fname[len(fname)-1]
                con.send(fname)
                with open(str(filename),"rb") as f:
                    data = f.read(1024)
                    print('Sending ...')
                    while(data):
                        con.send(data)
                        data = f.read(1024)

                time.sleep(1)
                print('Done!')
                print('Sent File ...')
                
                log['tokenDicom'] = token
                log['to'] = identities[0]
                log['toOrganization'] = identities[1]
                requests.post('http://%s:3000/api/shareDicom'%(self.HOST),json=log)

                print('Log added to Blockchain')

            
        con.close()     

    def start_transfer_dicom(self):
        while True:
            print('Server started ...')
            print('We have accepting connections')
            con, cliente = self.tcp.accept()
            print('Connected by ', cliente)
            start_new_thread(self.__server_socket,(con,)) 
        
        tcp.close()

    #Local Path images
    def registerDicom(self,hprovider, examType):
        try:
            paths = self.__readPathDicom(self.path)
            regs = self.__readAllDicom(paths,hprovider,examType)
            return True
        except:
            print('Error')

    # def shareDicom(path,amount):
    #     paths = __readPathDicom(path)
    #     sharefiles = readDicom(paths,amount)

    def audit(self,token):
        result = requests.get('http://%s3000/api/readAccessLog/%s'%(self.HOST,token))

        return result

class Clientsharedicom:

    def __init__(self,IP,PORT):
        self.HOST = IP  
        self.PORT = PORT

    def __isValidReseach(self,research):
        if (research == 'user1'):
            return True
        
        return False

    #req.body.tokenDicom, req.body.to, req.body.toOrganization
    def requestDicom(self,amount,research,org):
        if(self.__isValidReseach(research)):
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((self.HOST, self.PORT))
            tcp.send(pickle.dumps(amount))
            tcp.send(pickle.dumps(research))
            tcp.send(pickle.dumps(org))
            fname = tcp.recv(1024)
            print('fname: %s'%(fname))
            while(fname):
                fpath = os.path.join('~/SharedDicom',fname)
                if not os.path.exists('~/SharedDicom'):
                    os.mkdir('~/SharedDicom')

                f = open(fpath, 'wb+')
                l = tcp.recv(1024)
                print('Recieve ...')
                while (l):
                    f.write(l)
                    l = tcp.recv(1024)
                        
                print('Done ..')
                f.close()
                fname = tcp.recv(1024)
                print('fname: %s'%(fname))
            
            tcp.close()
