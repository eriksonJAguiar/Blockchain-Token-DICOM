from sharedicom import Clientsharedicom


if __name__ == "__main__":
    client = Clientsharedicom('10.62.9.185',5000)

    # Params:
    ### Request dicom images from blockchain network
    client.requestDicom(1,'user1','ICMC')
