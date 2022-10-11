import socket
import select
import sys
import os
import tqdm


BUFFER_SIZE = 4096
SEPARATOR = "<SEP>"


def connect(server_socket, input_socket):
    while True:
        try:
            read_ready, write_ready, exception = select.select(
                input_socket, [], [])

            for sock in read_ready:
                if sock == server_socket:
                    client_socket, client_address = server_socket.accept()
                    input_socket.append(client_socket)
                    print(f"Received connection from {client_address}")

                else:
                    data = sock.recv(BUFFER_SIZE)
                    if data:
                        file_name, file_size = data.decode(
                            'utf-8').split(SEPARATOR)
                        # print(f"{file_name} {file_size}")
                        download_file(sock, file_name, int(file_size))
                        print('closing socket')
                        sock.close()
                        input_socket.remove(sock)

                    else:
                        print('closing socket')
                        sock.close()
                        input_socket.remove(sock)

        except KeyboardInterrupt:
            server_socket.shutdown(socket.SHUT_RDWR)
            server_socket.close()
            sys.exit(0)


def download_file(socket, file_name, file_size):
    progress = tqdm.tqdm(
        range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(file_name, 'wb') as file:
        total = 0
        while True:
            bytes_read = socket.recv(BUFFER_SIZE)
            total += len(bytes_read)
            file.write(bytes_read)
            progress.update(len(bytes_read))
            if total == file_size:
                # print(f'Finished receiving {file_name}')
                break
        file.close()


if __name__ == "__main__":
    server_address = ('127.0.0.1', 5000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Waiting for connection...")
    input_socket = [server_socket]
    connect(server_socket, input_socket)
