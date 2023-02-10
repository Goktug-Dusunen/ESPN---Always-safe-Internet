import socket
import struct
import sys
import numpy as np
import tensorflow as tf
import hashlib
import hmac

def create_server(server_ip, server_port, secret_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (server_ip, server_port)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print("Waiting for a connection...")
        connection, client_address = sock.accept()

        try:
            message_length = struct.unpack("!Q", connection.recv(8))[0]
            message = connection.recv(message_length)
            nonce = message[:8]
            signature = message[8:]

            expected_signature = hmac.new(secret_key.encode('utf-8'), nonce, hashlib.sha256).digest()
            if signature != expected_signature:
                print("Invalid signature from client", client_address)
                continue

            connection.sendall(b'OK')

            data_length = struct.unpack("!Q", connection.recv(8))[0]
            data = connection.recv(data_length)
            analysis_result = analyze_network_data(data)
            print("Analysis result:", analysis_result)
            log_analysis_result(analysis_result, client_address)

        finally:
            connection.close()

def analyze_network_data(data):
    model = tf.keras.models.load_model("model.h5")
    prediction = model.predict(np.array(data))

    return prediction

def log_analysis_result(analysis_result, client_address):
    encrypted_log = encrypt_data(analysis_result)
    with open("analysis_log.txt", "a") as log_file:
        log_file.write(f"{client_address}: {encrypted_log}\n")

def encrypt_data(data):

    encrypted_data = "encrypted_data"
    return encrypted_data


server_ip = "127.0.0.1"
server_port = 8080
secret_key = "secret-key"

#re4p
create_server(server_ip, server_port, secret_key)
