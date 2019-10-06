import socket
import time
import traceback

import io

import constants
from model_server import ModelServer

try:
    import cPickle as pickle
except ImportError:
    import pickle

import json

global model_client

def load_models():
    # get model list from model_conf_path
    with open(constants.model_conf_path) as models_config:
        model_data = json.load(models_config)

    model_conf_list = model_data['model_conf_list']

    model_info_list = []

    for model in model_conf_list:
        model_info_list.append(model_conf_list[model])

    print(model_info_list)

    model_client = ModelServer(model_info_list)


def init_server_and_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    s.bind((constants.host, constants.port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

    try:
        while True:

            conn, addr = s.accept()  # Establish connection with client

            #we will be reading input values / tensors
            header_data = conn.recv(constants.header_size)
            header_str = header_data.decode().strip()

            total_bytes_received = b''

            while len(total_bytes_received) < no_of_top_file_bytes:
                remaining_bytes_to_read = no_of_top_file_bytes - len(total_bytes_received)

                if remaining_bytes_to_read > constants.data_size:
                    read_data = constants.data_size
                else:
                    read_data = remaining_bytes_to_read

                file_data = conn.recv(read_data)

                if not file_data:
                    break

                if file_data.endswith(b'Done'):
                    file_data_temp = file_data.replace(b'Done', b'')
                    total_bytes_received = total_bytes_received + file_data_temp
                else:
                    total_bytes_received = total_bytes_received + file_data

                if file_data.endswith(b'Done'):
                    break

            model_infer(model_name, input_values, conn)
    except Exception as e:
        traceback.print_exc()
    finally:
        s.close()


def model_infer(model_name, input_values, conn):
    try:
        t1 = time.time()

        infer_output = model_client.infer(model_name, input_values)

        send_response_back_to_client(conn, infer_output)

    except Exception as e:
        traceback.print_exc()


def send_response_back_to_client(conn, total_bytes_received):
    print("sending number of bytes: %s" % (len(total_bytes_received)))
    t1 = time.time()
    file = io.BytesIO(total_bytes_received)

    l = file.read(constants.data_size)

    while (l):
        conn.send(l)
        l = file.read(constants.data_size)

    conn.send(b'Done')
    t2 = time.time()
    print("Time taken for send_response_back_to_client: " + str(t2 - t1))


if __name__ == '__main__':
    load_models()
    init_server_and_listen()
