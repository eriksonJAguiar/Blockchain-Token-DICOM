from sharedicom import Serversharedicom


if __name__ == "__main__":
    server = Serversharedicom('../../DICOM_TCIA', 'localhost','10.62.9.23', 5000)

    # Params:
    # hprovider: healthcare provider to register dicom
    # typeExam: Type exam whithin dicom
    #print('Register images')
    #server.registerDicom('USP', 'Radiography')

    # let available server for transfer dicom
    server.start_transfer_dicom()
