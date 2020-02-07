from sharedicom import Clientsharedicom


if __name__ == "__main__":
    client = Clientsharedicom('localhost',5000)

    # Params:
    ### Request dicom images from blockchain network
    print('Request stated')
    client.requestDicom(1,'user1','ICMC')
    print('request finish')