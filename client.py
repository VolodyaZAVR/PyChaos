import socket
from main import Encoder
import logging


class Client(socket.socket):
    def __init__(self):
        super(Client, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def start_client(self, filename, connection="localhost", port=9999):
        self.connect((connection, port))
        self.send_file(filename)

    def send_file(self, filename):
        with open(filename, "rb") as file:
            while True:
                # read 1024 bytes from file
                file_data = file.read(1024)
                # sending 1024 bytes to server
                self.send(file_data)
                if not file_data:
                    break
        print(f"File sent: {filename}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s : %(levelname)s : %(message)s',
    )
    logging.debug(u"Начало программы")
    Encoder("input.jpg")
    Client().start_client('output.txt')
    