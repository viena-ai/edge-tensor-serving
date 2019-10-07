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

#TODO Use grpc
def init_server_and_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    s.bind((constants.host, constants.port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')
    model_name=''
    input_values=[]

    try:
        while True:
            conn, addr = s.accept()  # Establish connection with client

            int_byte_arr = conn.recv(4)

            if int_byte_arr.endswith(b'Done'):
                print("Done")
                break

            if len(int_byte_arr)<4:
                print("Error. Header has less than 4 bytes. need to handle this")
                break

            meta_data_len = int.from_bytes(int_byte_arr, byteorder='little')

            meta_data_byte_arr = conn.recv(meta_data_len)

            meta_data_str = meta_data_byte_arr.decode('utf-8')
            meta_data = meta_data_str.split(",")

            no_of_files = int(meta_data[0])

            total_bytes_received_image = b''
            curr_file_count = 1
            while curr_file_count <= no_of_files:
                no_of_file_bytes = int(meta_data[curr_file_count])
                out_name = str(curr_file_count)

                while len(total_bytes_received_image) < no_of_file_bytes:
                    remaining_bytes_to_read = no_of_file_bytes - len(total_bytes_received_image)

                    if remaining_bytes_to_read > constants.data_size:
                        read_data = constants.data_size
                    else:
                        read_data = remaining_bytes_to_read

                    file_data = conn.recv(read_data)

                    if not file_data:
                        break

                    total_bytes_received_image = total_bytes_received_image + file_data

                final_images = total_bytes_received_image

                img = pickle.loads(final_images)
                curr_file_count += 1


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
