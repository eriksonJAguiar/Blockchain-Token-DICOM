from sharedicom import Clientsharedicom


if __name__ == "__main__":
    client = Clientsharedicom('localhost',5000)

    # Params:
    ### Request dicom images from blockchain network
    client.requestDicom(1)