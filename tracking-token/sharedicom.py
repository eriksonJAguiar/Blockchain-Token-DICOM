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
import glob
from pydicom.datadict import tag_for_keyword
from pydicom.tag import Tag
from pathlib import Path
from shutil import make_archive
from pydicom.datadict import DicomDictionary, keyword_dict
from _thread import *
import shutil
import pandas as pd
import psutil
import struct
import zmq


class Serversharedicom:

    def __init__(self, path, IP, IPBC, PORT):
        self.path = path
        self.HOST = IP
        self.IPBC = str(IPBC)
        self.PORT = PORT
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind((self.HOST, self.PORT))
        self.tcp.listen(5)
        self.users = []
        self.cpu = []
        self.memory = []
        self.times = []
        self.time = 0

    def __isValidProvider(self, hprovider):

        try:
            if (hprovider in self.users):
                return True
            result = requests.post('http://%s:3000/api/registerUser' % (self.IPBC), json={
                                   'org': 'hprovider', 'user': hprovider, 'msp': 'HProviderMSP'})

            if(result.status_code == 200):
                self.users.append(hprovider)
                return True
        except:
            return False

    def __readPathDicom(self, path):

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

    def __readAllDicom(self, paths, owner, examType):
        files = []
        for path_ in paths:
            try:
                result = list(Path(path_).rglob("*.dcm"))
                image = pydicom.dcmread(str(result[0]))

                dicomId = image.data_element('SOPInstanceUID').value

                requests.post('http://%s:3000/api/createDicom' % (self.IPBC), json={
                              'user': owner, 'dicomId': dicomId, 'typeExam': examType, 'owner': owner})
            except:
                print('%s File not register' % (dicomId))
                exit(1)

        print('Regiter Successful')

    def __readDicom(self, paths, amount):
        pathzip = []
        tokens = []
        if (amount > len(paths)):
            amount = len(paths)-1
        for i in range(amount):
            rd = random.randint(0, len(paths)-1)
            path_ = paths[rd]

            # result = list(Path(path_).rglob("*.dcm"))
            result = glob.glob(os.path.join(path_, "*.dcm"))
            image = pydicom.dcmread(str(result[0]))

            dicomId = image.data_element('PatientID').value
            t = str(datetime.datetime.now().timestamp())
            value = str(dicomId)+t
            sha = hashlib.sha256()
            sha.update(value.encode('utf-8'))
            token = sha.hexdigest()

            zipname = '%s.zip' % (token)
            newpath = os.path.join(self.path, 'shared')
            os.makedirs(newpath, exist_ok=True)

            newzip = os.path.join(self.path, 'shared-zip')
            os.makedirs(newzip, exist_ok=True)
            zf = zipfile.ZipFile(os.path.join(newzip, zipname), "w")

            for res in result:
                fname = str(res).split('/')
                fname = fname[len(fname)-1]
                image = pydicom.dcmread(str(res))
                new_tag = ((0x08, 0x17))
                image.add_new(new_tag, 'CS', token)
                image.save_as(os.path.join(newpath, fname))
                zf.write(os.path.join(newpath, fname), arcname=fname)

            shutil.rmtree(newpath)
            pathzip.append(os.path.join(newzip, zipname))
            tokens.append(token)

        return pathzip, tokens

    # req.body.tokenDicom, req.body.to, req.body.toOrganization
    def __server_socket(self, con):
        # amount = pickle.loads(con.recv())
        # time.sleep(1)
        # user = con.recv().decode('utf8')
        # time.sleep(1)
        # org = con.recv().decode('utf8')
        # time.sleep(1)
        cred = pickle.loads(con.recv(4096))
        print(cred)
        amount = cred['amount']
        paths = self.__readPathDicom(self.path)
        sharefiles, tokens = self.__readDicom(paths, amount)
        for filename, token in zip(sharefiles, tokens):
            fname = filename.split('/')
            fname = fname[len(fname)-1]
            con.send(fname.encode('utf8'))
            with open(str(filename),"rb") as f: 
                size = os.path.getsize(filename)
                s = 0
                while s <= size:
                    fl = f.read(1024)
                    con.send(fl)
                    s += len(fl)


            print('Done!')
            print('Sent File ...')

            # process = psutil.Process(os.getpid())
            # start_new_thread(self.__mensure, (process,))
            self.cpu.append(process.cpu_percent())
            self.memory.append(process.memory_percent())
            self.times.append(self.time)
            self.time +=1
             
            requests.post('http://%s:3000/api/shareDicom'%(self.IPBC),json={'user': cred['user'],'tokenDicom':token, 'to': cred['user'], 'toOrganization': cred['org']})
            
            print('Log added to Blockchain')

            time.sleep(1)
            
        shutil.rmtree(os.path.join(self.path,'shared-zip'))
        tabela = pd.DataFrame()
        tabela.insert(0, "Time", self.times)
        tabela.insert(1, "Usage Memory", self.memory)
        tabela.insert(2,"Usage CPU", self.cpu)
        tabela.to_csv('../Results/table_Performance_%s.csv'%(datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S")),sep=';')
        con.close()
        con.destroy()     

    def start_transfer_dicom(self,hprovider):
        if(self.__isValidProvider(hprovider)):
            try:
                while True:
                    print('Server started ...')
                    print('We have accepting connections in %s:%s'%(self.HOST,self.PORT))
                    con, cliente = self.tcp.accept()
                    print('Connected by ', cliente)
                    start_new_thread(self.__server_socket,(con,)) 
            except KeyboardInterrupt:
                tcp.close()
                
        
            

    # Local Path images
    def registerDicom(self,hprovider, examType):
        try:
            if(self.__isValidProvider(hprovider)):
                paths = self.__readPathDicom(self.path)
                regs = self.__readAllDicom(paths,hprovider,examType)
                return True
            
            return False
        except:
            print('Error')

    # def shareDicom(path,amount):
    #     paths = __readPathDicom(path)
    #     sharefiles = readDicom(paths,amount)

    def audit(self,token,hprovider):
        result = requests.get('http://%s:3000/api/readAccessLog'%(self.IPBC), params={'tokenDicom':token, 'user': hprovider})

        return result

class Clientsharedicom:

    def __init__(self,IP,PORT):
        self.HOST = IP  
        self.PORT = PORT
        self.users = []

    def __isValidReseach(self,research):
        
        if (research in self.users):
            return True
        
        result = requests.post('http://%s:3000/api/registerUser'%(self.HOST), json={'org':'research', 'user':research, 'msp': 'ResearchMSP'})
        
        if(result.status_code == 200):
            self.users.append(research)
            return True
        

        return False
        
    # req.body.tokenDicom, req.body.to, req.body.toOrganization
    def requestDicom(self,amount,research,org):
        time_file = []
        block_size = []
        if(self.__isValidReseach(research)):
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((self.HOST, self.PORT))
            # tcp.send(pickle.dumps(amount))
            # time.sleep(1)
            # tcp.send(research.encode('utf8'))
            # tcp.sleep(1)
            # tcp.send(org.encode('utf8'))
            json_credentials = {'amount': amount, 'user': research, 'org': org}
            tcp.sendall(pickle.dumps(json_credentials))
            fname = str(tcp.recv(1024).decode('utf8'))
            while(fname):
                start_time_file = time.time()
                size_block = 0
                print('fname: %s'%(fname))
                fpath = os.path.join('../SharedDicom',fname)
                if not os.path.exists('../SharedDicom'):
                    os.mkdir('../SharedDicom')

                f = open(fpath, 'wb+')
                l = tcp.recv(1024)
                size_block += sys.getsizeof(l)
                print('Recieve ...')
                while (l):
                    f.write(l)
                    l = tcp.recv()
                    size_block += sys.getsizeof(l)
                f.close()        
                print('Done ..')
                time_file.append(time.time()-start_time_file)
                block_size.append(size_block*0.001)
                fname = str(tcp.recv().decode('utf8'))
                time.sleep(1)
            
            tcp.close()
           
        return(time_file, block_size)
            
