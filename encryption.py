from cryptography.fernet import Fernet
import hashlib


class PasswordHelper:
    """
    class object to help with hashing the password
    references: https://docs.python.org/3/library/hashlib.html 
    """
    @staticmethod
    def hash_pw(password=""):
        """
        :param password: message to hash
        :return: hex digitised 64 character hash
        """
        password_bit = password.encode()
        return hashlib.sha256(password_bit).hexdigest()


class EncryptionHelper:
    """
    object for loading the encryption key
    references: https://nitratine.net/blog/post/encryption-and-decryption-in-python/#reading-keys
    """
    def __init__(self, key_path="secure/GPDB.key"):
        """
        :param key_path: specify path to key leave blank for default
        """
        file = open(key_path, 'rb')
        self.key = file.read()
        self.cipher = Fernet(self.key)
        file.close()
    
    def encrypt_to_bits(self, info="") -> str:
        """
        :param str info: information in string for encoding
        :return: bit object for storage in DB
        """
        to_bit_message = info.encode()
        encrypted_message = self.cipher.encrypt(to_bit_message)
        return encrypted_message

    def decrypt_message(self, ciphered_text=b''):
        """
        :param ciphered_text: information in string for encoding
        :return: bit object for storage in DB
        """
        decrypted_bits = self.cipher.decrypt(ciphered_text)
        message = decrypted_bits.decode()
        return message


# if __name__ == "__main__":
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
