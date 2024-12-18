import sys
import pickle
import socket
import threading

from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QApplication
from gui import Ui_MainWindow

class CityGameClient(QObject):
    msg_recv = pyqtSignal(str)

    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        while True:
            try:
                message = pickle.loads(self.client_socket.recv(1024))
                if message:
                    self.msg_recv.emit(message)
                else:
                    break
            except:
                break

    def start(self):
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print("Подключено к серверу")
        except Exception as e:
            print(f"Не удалось подключиться к серверу: {e}")
            return

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_msg(self, message):
        try:
            self.client_socket.send(pickle.dumps(message))
        except Exception as e:
            print(f"Не удалось отправить сообщение: {e}")

    def close(self):
        self.client_socket.close()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, client: CityGameClient):
        super().__init__()
        self.client = client
        self.setupUi(self)
        self.setWindowTitle("City Game")
        self.send_button.clicked.connect(self.send_message)
        self.create_button.clicked.connect(self.create_game)
        self.join_button.clicked.connect(self.join_game)
        self.exit_button.clicked.connect(self.exit_game)
        self.ban_button.clicked.connect(self.ban_player)
        self.client.msg_recv.connect(self.update_output)
        self.show()

    def send_message(self):
        message = self.input.text()
        self.client.send_msg(message)
        self.output.append(f"You: {message}")
        self.input.clear()

    def create_game(self):
        self.client.send_msg("create")

    def join_game(self):
        self.client.send_msg("join")

    def exit_game(self):
        self.client.send_msg("exit")

    def ban_player(self):
        self.client.send_msg("ban")

    @pyqtSlot(str)
    def update_output(self, message):
        self.output.append(message)

    def closeEvent(self, event):
        self.client.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = CityGameClient('localhost', 12357)
    client.start()
    window = MainWindow(client)
    window.show()
    sys.exit(app.exec())
