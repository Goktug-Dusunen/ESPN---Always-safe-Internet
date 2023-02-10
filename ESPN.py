import socket
import struct
import sys
import numpy as np
import tensorflow as tf
import hashlib
import hmac
import os
#ats

import time
import sys

def loading_animation():
    spinners = ['|', '/', '-', '\\']
    for i in range(50):
        for spinner in spinners:
            os.system('figlet ESPN')
            sys.stdout.write(f"\r{spinner} Loading... ")
            sys.stdout.flush()
            time.sleep(0.1)

loading_animation()
def create_tunnel(server_ip, server_port, secret_key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (server_ip, server_port)
    sock.connect(server_address)


    nonce = struct.pack("!Q", np.random.randint(0, 2**64-1))


    signature = hmac.new(secret_key.encode('utf-8'), nonce, hashlib.sha256).digest()


    message = nonce + signature
    sock.sendall(struct.pack("!Q", len(message)) + message)


    response_length = struct.unpack("!Q", sock.recv(8))[0]
    response = sock.recv(response_length)
    if response == b'OK':
        print("Tunnel created successfully!")
    else:
        print("Failed to create the tunnel.")


    sock.close()

def analyze_network_data(data):

    model = tf.keras.models.load_model("model.h5")
    prediction = model.predict(np.array(data))


    return prediction

# Example usage
server_ip = "127.0.0.1"
server_port = 8080
secret_key = "secret-key"


create_tunnel(server_ip, server_port, secret_key)


data = [1, 2, 3, 4, 5]
result = analyze_network_data(data)
print("Analysis result:", result)
