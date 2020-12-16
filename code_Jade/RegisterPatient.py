import databaseHelp


def insertIntoDB():
    """"""
    insertNewPatient = databaseHelp.SQLQuerry("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    encryptionHelper = databaseHelp.encryptionHelper()
    insertNewPatient.executeCommit(("G01", "testPatient",
                                             databaseHelp.passwordHelper.hashPW("testPatientPW"),
                                             encryptionHelper.encryptToBits("testPatientFirstName"),
                                             encryptionHelper.encryptToBits("testPatientLastName"),
                                             encryptionHelper.encryptToBits("0123456789"),
                                             encryptionHelper.encryptToBits("testPatientHome Address, testing street"),
                                             encryptionHelper.encryptToBits("TW 8FGT"),
                                             "Patient",
                                             "M"))


if __name__ == '__main__':
    # test user inputs before inserting into database using insertIntoDB function
    pass
