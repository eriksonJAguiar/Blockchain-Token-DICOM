from sharedicom import Serversharedicom
import sys
import os

if __name__ == "__main__":
    server = Serversharedicom('/media/erjulioaguiar/DFE1-F19A/DICOM_TCIA/', '10.62.9.185','10.62.9.185', 5001)

    # Params:
    # hprovider: healthcare provider to register dicom
    # typeExam: Type exam whithin dicom
    #print('Register images')
    # val = 0
    # val = sys.argv[0]
    # if(val == 1):
    #     server.registerDicom('USP', 'Radiography')

    # let available server for transfer dicom
    #server.start_transfer_dicom('USP')
    print(os.getegid())
    server.start_transfer()
