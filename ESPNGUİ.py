import sys
import socket
import struct
import numpy as np
import tensorflow as tf
import hashlib
import hmac
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import QRect, QPropertyAnimation
#granitlio
class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server_ip = "127.0.0.1"
        self.server_port = 8080
        self.secret_key = "secret-key"
        self.setWindowTitle("Network Data Analyzer")
        self.setGeometry(400, 400, 500, 500)
        self.connect_button = QPushButton("Bağlan", self)
        self.connect_button.setGeometry(QRect(200, 200, 100, 50))
        self.connect_button.clicked.connect(self.connect_to_server)
        self.exit_button = QPushButton("Çık", self)
        self.exit_button.setGeometry(QRect(200, 300, 100, 50))
        self.exit_button.clicked.connect(self.close_application)
        self.show()

    def connect_to_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.server_ip, self.server_port)
        sock.connect(server_address)
        nonce = struct.pack("!Q", np.random.randint(0, 2**64-1))
        signature = hmac.new(self.secret_key.encode('utf-8'), nonce, hashlib.sha256).digest()
        message = nonce + signature
        sock.sendall(struct.pack("!Q", len(message)) + message)
        response_length = struct.unpack("!Q", sock.recv(8))[0]
        response = sock.recv(response_length)
        if response == b'OK':
            QMessageBox.about(self, "Başarılı", "Bağlantı başarılı oluşturuldu!")
        else:
            QMessageBox.warning(self, "Başarısız", "Bağlantı oluşturulamadı!")
        sock.close()

    def close_application(self):
        choice = QMessageBox.question(self, "Çıkış", "Çıkmak istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
