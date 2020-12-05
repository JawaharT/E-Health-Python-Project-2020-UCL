from os import stat
from cryptography.fernet import Fernet

import hashlib
class passwordHelper():
    """
    class object to help with hashing the password
    references: https://docs.python.org/3/library/hashlib.html 
    """
    @staticmethod
    def hashPW(password=""):
        """
        :param password: message to hash
        :return: hexdigested 64 character hash
        """
        passwordBit = password.encode()
        return hashlib.sha256(passwordBit).hexdigest()
        



class encryptionHelper():
    '''
    object for loading the encryption key
    references: https://nitratine.net/blog/post/encryption-and-decryption-in-python/#reading-keys
    '''
    def __init__(self, keyPath="secure/GPDB.key"):
        """
        :param key: specify path to key leave blank for default
        """
        file = open(keyPath, 'rb')
        self.key = file.read()
        self.cipher = Fernet(self.key)
        file.close()
    
    def encryptToBits(self, info=""):
        """
        :param info: information in string for encoding
        :return: bit object for storage in DB
        """
        toBitMessage = info.encode()
        encryptedMessage = self.cipher.encrypt(toBitMessage)
        return encryptedMessage

    def decryptMessage(self, cipheredText=b''):
        """
        :param info: information in string for encoding
        :return: bit object for storage in DB
        """
        decryptedbits = self.cipher.decrypt(cipheredText)
        message = decryptedbits.decode()
        return message
    
        



if __name__ == "__main__":
    # ##never uncomment this code unless you are very sure yu need to this will generate and overwrite the existing key might damage all data
    # key = Fernet.generate_key()
    # file = open('secure/GPDB.key', 'wb+')  # Open the file as wb to write bytes
    # file.write(key)  # The key is type bytes still
    # file.close()

    # ## test fo encrypt and decrypt function
    # EH = encryptionHelper()
    # encrypted = EH.encryptToBits("testing testing 1234 ,.'!?$% &()^")
    # print(type(encrypted))
    # decrypted = EH.decryptMessage(encrypted)
    # print(decrypted)

    # ##test for hashing PW
    # password = "1293495!!?$&"
    # hash = passwordHelper.hashPW(password)
    # print(type(hash))
    # print(hash)
    pass