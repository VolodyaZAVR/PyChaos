import socket
from main import Decoder
import logging

class Server(socket.socket):
    def __init__(self):
        super(Server, self).__init__(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.bind(("localhost", 9999))
        self.listen(5)

    def start_server(self):
        print("Server is started.")
        connection, address = self.accept()
        print("Connected: ", address)
        self.listen_connection(connection)
        connection.close()
        print("Connection was closed")

    @staticmethod
    def listen_connection(user_connection=None, filename="received.txt"):
        with open(filename, "wb") as outfile:
            while True:
                data = user_connection.recv(1024)
                if not data:
                    print(f"End of receiving file {outfile}.")
                    break
                outfile.write(data)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s : %(levelname)s : %(message)s',
    )
    Server().start_server()
    Decoder("received.txt")
    logging.debug(u"Конец программы")