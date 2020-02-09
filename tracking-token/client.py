from sharedicom import Clientsharedicom
import random

if __name__ == "__main__":
    client = Clientsharedicom('10.62.9.185',5001)

    # Params:
    ### Request dicom images from blockchain network
    print('Request stated')
    client.requestDicom(1,'erikson','ICMC')
    print('request finish')