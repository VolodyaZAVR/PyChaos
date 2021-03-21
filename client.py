import socket
from main import Encoder, Decoder
import logging
import sys


class Client(socket.socket):
    def __init__(self):
        super(Client, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def start_client(self, filename, connection="localhost", port=9999):
        self.connect((connection, port))
        self.listen_server(filename)

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

    def listen_server(self, filename="src/received.txt"):
        with open(filename, "wb") as outfile:
            while True:
                data = self.recv(1024)
                if not data:
                    print(f"End of receiving file {outfile}.")
                    break
                outfile.write(data)


if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s : %(levelname)s : %(message)s',
        )
        logging.debug(u"Начало программы")
        Encoder(sys.argv[1])
        logging.debug(u"Сервер подключается к серверу")
        Client().start_client('src/output.txt')
        logging.debug(u"Запуск декодера")
        Decoder("src/received.txt")
        logging.debug(u"Конец программы")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
