import sys
import os
from encryption.RC4 import RC4

available_methods = ("aes", "des", "rc4")
encryptor = {"rc4": RC4()}

input_message = [
    '\r----------',
    'Available commands:',
    '/send <AES/DES/RC4> <file>          Send an encrypted file to server',
    '/decrypt <AES/DES/RC4> <file>       Decrypt an encrypted file',
    '/quit                               Exit the app',
    '----------',
    '>> '
]

return_code = {1: "file sent successfully", 2: "file decrypted",
               -1: "file not found", -2: "Method unavailable"}


def print_command():
    print('\n'.join(input_message), end='')


def send_file(filePath):
    pass


def encrypt_and_send(method, file):
    method = method.lower()
    if method not in available_methods:
        return -2
    elif not os.path.isfile(file):
        return -1
    else:
        enc_file_path = encryptor[method].encrypt(file)
        send_file(enc_file_path)
        return 1


def decrypt(method, file):
    method = method.lower()
    if method not in available_methods:
        return -2
    elif not os.path.isfile(file):
        return -1
    else:
        dec_file_path = encryptor[method].decrypt(file)
        send_file(dec_file_path)
        return 2


if __name__ == "__main__":
    print_command()
    while True:
        commands = input()
        available_commands = ('/send', '/decrypt', '/quit')

        command = commands.split(" ", 2)

        if command[0] not in available_commands:
            print(
                f'\rCommand {command[0]} not found.\n----------\n>> ', end='')
        elif command[0] == available_commands[0]:
            result = encrypt_and_send(method=command[1], file=command[2])
            print(return_code[result])
        elif command[0] == available_commands[1]:
            result = decrypt(method=command[1], file=command[2])
            print(return_code[result])
        else:
            sys.exit()
        print_command()
