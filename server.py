import socket


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
        self.send_file()
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

    def send_file(self, filename="output.txt"):
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
    Server().start_server()
