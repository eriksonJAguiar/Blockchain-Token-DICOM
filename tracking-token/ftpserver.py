from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os


def ftp_server(path):
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", os.path.join(path, 'shared-zip/'), perm="elradfmw") 
    authorizer.add_anonymous(os.path.join(path, 'shared-zip/'), perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('10.62.9.185', 1026), handler)
    server.serve_forever()

if __name__ == "__main__":
    ftp_server('/media/erjulioaguiar/DFE1-F19A/DICOM_TCIA/')
     