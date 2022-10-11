import sys
import os
import socket
import tqdm
from encryption.RC4 import RC4
from encryption.AES_Library import AES_L
from encryption.DES import DES_L

available_methods = ("aes", "des", "rc4")
encryptor = {"rc4": RC4(),"aes": AES_L(), "des": DES_L()}
BUFFER_SIZE = 4096
SEPARATOR = "<SEP>"

input_message = [
    '\r----------',
    'Available commands:',
    '/send <AES/DES/RC4> <file full path>          Send an encrypted file to server',
    '/decrypt <AES/DES/RC4> <file full path>       Decrypt an encrypted file',
    '/quit                                         Exit the app',
    '----------',
    '>> '
]

return_code = {1: "file sent successfully", 2: "file decrypted",
               -1: "file not found", -2: "Method unavailable"}


def print_command():
    print('\n'.join(input_message), end='')


def send_file(filePath):
    server_address = ('127.0.0.1', 5000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    file_name = os.path.basename(filePath)
    file_size = os.path.getsize(filePath)

    client_socket.sendall(f"{file_name}{SEPARATOR}{file_size}".encode())

    progress = tqdm.tqdm(range(
        file_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filePath, 'rb') as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            progress.update(len(bytes_read))
            if not bytes_read:
                # print(f'Finished sending {file_name}')
                break
            client_socket.sendall(bytes_read)
        file.close()

    client_socket.close()


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
        encryptor[method].decrypt(file)
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
            result = encrypt_and_send(
                method=command[1], file=command[2].strip('"'))
            print(return_code[result])
        elif command[0] == available_commands[1]:
            result = decrypt(method=command[1], file=command[2])
            print(return_code[result])
        else:
            sys.exit()
        print_command()
