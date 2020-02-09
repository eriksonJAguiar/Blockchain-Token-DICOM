from sharedicom import Clientsharedicom
import random

if __name__ == "__main__":
    client = Clientsharedicom('10.62.9.185',5001)

    # Params:
    ### Request dicom images from blockchain network
    
    for i in range(30):
        rd = random.randint(1,50)
        print('Request stated for %i files'%(rd))
        client.requestDicom(rd,'erikson','ICMC')
        print('request finish')