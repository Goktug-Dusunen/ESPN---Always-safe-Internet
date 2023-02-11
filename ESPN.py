import socket
import ssl
import numpy as np
import tensorflow as tf
#ats
def loading_animation():
    spinners = ['|', '/', '-', '\\']
    for i in range(50):
        for spinner in spinners:
            os.system('figlet ESPN')
            sys.stdout.write(f"\r{spinner} Loading... ")
            sys.stdout.flush()
            time.sleep(0.1)
def start_client():

    model = tf.keras.models.load_model('encryption_model.h5')


    key = generate_key(model)


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 12345)
    client_socket.connect(server_address)


    context = ssl.create_default_context()
    secured_socket = context.wrap_socket(client_socket, server_hostname='localhost')


    message = 'Hello, server!'
    encrypted_data = encrypt_data(message.encode(), key)


    secured_socket.sendall(encrypted_data)


    encrypted_data = secured_socket.recv(1024)


    data = decrypt_data(encrypted_data, key)
    print('Received data from server:', data.decode())


    secured_socket.close()
    client_socket.close()

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

if __name__ == '__main__':
    start_client()
