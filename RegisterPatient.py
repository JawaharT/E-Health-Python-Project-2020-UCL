import database_help


def insertIntoDB():
    """"""
    insertNewPatient = database_help.SQLQuery("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    encryptionHelper = database_help.encryptionHelper()
    insertNewPatient.executeCommit(("G01", "testPatient",
                                    database_help.passwordHelper.hashPW("testPatientPW"),
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
