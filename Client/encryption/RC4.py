import os


class RC4():
    def __init__(self):
        self.key = "YXUCYRDV"
        self.keyBytes = []

        for byte in self.key:
            self.keyBytes.append(ord(byte))

    def crypt(self, fileBytes, keyBytes):

        cipherList = []

        keyLen = len(keyBytes)
        fileLen = len(fileBytes)
        S = [i for i in range(256)]

        j = 0
        for i in range(256):
            j = (j + S[i] + keyBytes[i % keyLen]) % 256
            S[i], S[j] = S[j], S[i]

        i = 0
        j = 0
        for m in range(fileLen):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            cipherList.append(k ^ fileBytes[m])

        return cipherList

    def encrypt(self, file):
        file_name = os.path.basename(file)
        enc_file_name = file_name + ".enc"
        enc_file_path = os.path.join(os.getcwd(), enc_file_name)
        print(f"enc file path = {enc_file_path}")

        with open(file, "rb") as in_file:
            stream = in_file.read()
            plainBytes = list(stream)

        cipherList = self.crypt(plainBytes, self.keyBytes)

        with open(enc_file_path, "wb") as out_file:
            out_file.write(bytes(cipherList))

        return enc_file_path

    def decrypt(self, file):
        with open(file, 'rb') as in_file:
            stream = in_file.read()
            cipherBytes = list(stream)

        file_name = os.path.basename(file)
        dec_file_name = ".".join(file_name.split('.')[:-1])
        dec_file_path = os.path.join(os.getcwd(), dec_file_name)

        plainList = self.crypt(cipherBytes, self.keyBytes)

        with open(dec_file_path, 'wb') as out_file:
            out_file.write(bytes(plainList))

        return dec_file_path
