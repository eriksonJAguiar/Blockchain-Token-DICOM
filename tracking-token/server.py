from sharedicom import Serversharedicom


if __name__ == "__main__":
    server = Serversharedicom('../../DICOM_TCIA', '127.0.0.1', 5000)

    # Params:
    # hprovider: healthcare provider to register dicom
    # typeExam: Type exam whithin dicom
    #server.registerDicom('USP', 'Radiography')

    # let available server for transfer dicom
    server.start_transfer_dicom()
