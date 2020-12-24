import DatabaseHelp


def insertIntoDB():
    insertNewAdmin = DatabaseHelp.SQLQuerry("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    encryptionHelper = DatabaseHelp.encryptionHelper()
    insertNewAdmin.executeCommit(("A01", "testAdmin",
                                  DatabaseHelp.passwordHelper.hashPW("testAdminPW"),
                                  encryptionHelper.encryptToBits("testAdminFirstName"),
                                  encryptionHelper.encryptToBits("testAdminLastName"),
                                  encryptionHelper.encryptToBits("0123456789"),
                                  encryptionHelper.encryptToBits("testAdminHome Address, testing street"),
                                  encryptionHelper.encryptToBits("TW 8FGT"),
                                  "Admin",
                                  "M"))


if __name__ == '__main__':
    # test user inputs before inserting into database using insertIntoDB function
    pass
