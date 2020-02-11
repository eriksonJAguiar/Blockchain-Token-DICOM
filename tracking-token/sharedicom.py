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
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP


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

    def __mensure(self):
        a = dict(psutil.virtual_memory()._asdict())
        self.cpu.append(psutil.cpu_percent())
        self.memory.append(a['used']/1073741824)
        self.times.append(self.time)
        self.time += 1

    # req.body.tokenDicom, req.body.to, req.body.toOrganization
    def __server_socket(self, con):
        cred = pickle.loads(con.recv(4096))
        amount = cred['amount']
        paths = self.__readPathDicom(self.path)
        sharefiles, tokens = self.__readDicom(paths, amount)
        con.sendall(pickle.dumps(sharefiles))
        com.close()
        self.__mensure()

        for tk in tokens:
            requests.post('http://%s:3000/api/shareDicom' % (self.IPBC), json={
                          'user': cred['user'], 'tokenDicom': tk, 'to': cred['user'], 'toOrganization': cred['org']})
            print('Log added to Blockchain')

        tabela = pd.DataFrame()
        tabela.insert(0, "Time", self.times)
        tabela.insert(1, "Usage Memory", self.memory)
        tabela.insert(2, "Usage CPU", self.cpu)
        tabela.to_csv('../Results/table_Performance_%s.csv' %
                      (datetime.datetime.now().strftime("%m%d%Y_%H:%M:%S")), sep=';')
        
        # delfile = pickle.loads(con.recv(1024))
        # if delfile:
        # shutil.rmtree(os.path.join(self.path,'shared-zip'))
        con.close()

    def start_transfer_dicom(self):
        try:
             while True:
                print('Server started ...')
                print('We have accepting connections in %s:%s'%(self.HOST,self.PORT))
                con, cliente = self.tcp.accept()
                print('Connected by ', cliente)
                start_new_thread(self.__server_socket,(con,)) 
        except KeyboardInterrupt:
            tcp.close()

    
    def start_transfer(self):
        self.start_transfer_dicom()
        

    # Local Path images
    def registerDicom(self, hprovider, examType):
        try:
            if(self.__isValidProvider(hprovider)):
                paths = self.__readPathDicom(self.path)
                regs = self.__readAllDicom(paths, hprovider, examType)
                return True

            return False
        except:
            print('Error')


    def audit(self, token, hprovider):
        result = requests.get('http://%s:3000/api/readAccessLog' %
                              (self.IPBC), params={'tokenDicom': token, 'user': hprovider})

        return result


class Clientsharedicom:

    def __init__(self, IP, PORT):
        self.HOST = IP
        self.PORT = PORT
        self.users = []
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.connect((self.HOST, self.PORT))

    def __isValidReseach(self, research):

        if (research in self.users):
            return True

        result = requests.post('http://%s:3000/api/registerUser' % (self.HOST), json={
                               'org': 'research', 'user': research, 'msp': 'ResearchMSP'})

        if(result.status_code == 200):
            self.users.append(research)
            return True

        return False

    # req.body.tokenDicom, req.body.to, req.body.toOrganization
    def requestDicom(self, amount, research, org):
        time_file = []
        block_size = []
        
        if(self.__isValidReseach(research)):
            json_credentials = {'amount': amount, 'user': research, 'org': org}
            self.tcp.send(pickle.dumps(json_credentials))
            files = pickle.loads(self.tcp.recv(4096))
            os.makedirs('../SharedDicom', exist_ok=True)
            ftp = FTP()
            ftp.connect('10.62.9.185', 1026)
            ftp.login(user='user', passwd = '12345')
            ftp.cwd('/media/erjulioaguiar/DFE1-F19A/DICOM_TCIA/shared-zip/')
            #ftp.retrlines('LIST')
            for filename in files:
                # start_time_file = time.time()
                fname = filename.split('/')
                fname = fname[len(fname)-1]
                fpath = os.path.join('../SharedDicom', fname)
                localfile = open(os.path.join('../SharedDicom', fname), 'wb')
                ftp.retrbinary('STOR ' + fname, localfile.write, 1024)
                localfile.close()
                print('Done ..')
                # time_file.append(time.time()-start_time_file)
                # block_size.append(buffsize*0.001)

                # time.sleep(1)
            ftp.quit()
            time.sleep(1)
            self.tcp.send(pickle.dumps(True))
            
            self.tcp.close()

        # return(time_file, block_size)
