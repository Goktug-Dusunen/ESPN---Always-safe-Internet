import socket
import ssl
import numpy as np
import tensorflow as tf
#grantilio
def start_server():

    encryption_model = tf.keras.models.load_model('encryption_model.h5')
    attack_detection_model = tf.keras.models.load_model('attack_detection_model.h5')


    key = generate_key(encryption_model)


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    server_address = ('localhost', 12345)
    server_socket.bind(server_address)


    server_socket.listen(1)

    print('Waiting for a client to connect...')
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from', client_address)


    context = ssl.create_default_context()
    secured_socket = context.wrap_socket(client_socket, server_side=True)

    while True:

        encrypted_data = secured_socket.recv(1024)


        data = decrypt_data(encrypted_data, key)
        print('Received data from client:', data.decode())


        is_attack = detect_attack(data, attack_detection_model)
        if is_attack:
            print('Detected an attack! Closing the connection.')
            break


        message = 'Hello, client!'
        encrypted_data = encrypt_data(message.encode(), key)


        secured_socket.sendall(encrypted_data)


    secured_socket.close()
    client_socket.close()
    server_socket.close()

def generate_key(model):

    input_data = np.random.rand(1, 100)


    key = model.predict(input_data)

    return key

def encrypt_data(data, key):

    encrypted_data = np.bitwise_xor(data, key)

    return encrypted_data

def decrypt_data(encrypted_data, key):

    data = np.bitwise_xor(encrypted_data, key)

    return data

def detect_attack(data, model):

    input_data = np.array(data).reshape(1, -1)
    prediction = model.predict(input_data)

    return True if prediction[0][0] >= 0.5 else False

if __name__ == '__main__':
    start_server()
