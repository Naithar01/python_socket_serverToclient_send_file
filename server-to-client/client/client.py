import socket
import threading

import datetime

def RecvMsg(client):
    while True:
        msg = client.recv(8192)

        if msg:
            save_file_name = datetime.datetime.now()

            file = open(str(save_file_name).replace(":", " ") +'.jpg', "wb")
            file.write(msg)

            file.close()


def SendMsg(client):
    while True:
        try:
            send_msg = input()

            if len(send_msg) == 0:
                print("Close Client")
                break

            file = open(send_msg, 'rb')
            image_data = file.read(8192)

            client.send(image_data)

            file.close()

        except:
            client.close()
            print('Some Error')
            break

def ConnectServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1002))

    while True:
        try:
            # recv_thread = threading.Thread(target=RecvMsg, args=(client, ))
            send_thread = threading.Thread(target=SendMsg, args=(client, ))
            
            # recv_thread.start()
            send_thread.start()
            RecvMsg(client)

        except:
            client.close()
            break


ConnectServer()