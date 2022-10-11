from Crypto import Random
from Crypto.Cipher import DES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class DES_L:
    def __init__(self):
        self.key = b"-9A KEY-"

    def pad(self, s):
        return s + b"\0" * (DES.block_size - len(s) % DES.block_size)

    def encrypting(self, message, key, key_size=256):
        message = self.pad(message)
        des_nonce = b'3A'
        cipher = DES.new(key, DES.MODE_CTR, nonce=des_nonce)
        return cipher.encrypt(message)

    def encrypt(self, file_name):
        enc_file_name = file_name + ".enc"
        enc_file_path = os.path.join(os.getcwd(), enc_file_name)
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypting(plaintext, self.key)
        with open(enc_file_name, 'wb') as fo:
            fo.write(enc)

        return enc_file_path

    def decrypting(self, ciphertext, key):
        des_nonce = b'3A'
        cipher = DES.new(key, DES.MODE_CTR, nonce=des_nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.rstrip(b"\0")

    def decrypt(self, file_name):
        
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypting(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
