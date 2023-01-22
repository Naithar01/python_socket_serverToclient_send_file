import socket
import threading

import datetime

def RecvMsg(connect_client):
    while True:
        msg = connect_client.recv(2048)

        if msg:
            save_file_name = datetime.datetime.now()

            file = open(str(save_file_name).replace(":", " ") +'.jpg', "wb")
            file.write(msg)
            file.close() 


def SendMsg(connect_client, server):
    while True:
        try:
            send_msg = input()

            if len(send_msg) == 0:
                server.close()
                connect_client.close()
                print("Close Server")
                break


            if send_msg:
                file = open(send_msg, 'rb')
                image_data = file.read(8192)

                connect_client.send(image_data)

                file.close() 

        except:
            connect_client.close()
            print('Some Error')
            break

def CreateServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('localhost', 1002)) 
    server.listen()

    print("Server is Running...")

    while True:
        try:
            connect_client, connect_client_address = server.accept()

            print(f"Connect {connect_client_address}")

            # recv_thread = threading.Thread(target=RecvMsg, args=(connect_client, ))
            send_thread = threading.Thread(target=SendMsg, args=(connect_client, server))

            # recv_thread.start()

            send_thread.start()

            RecvMsg(connect_client)
        except:
            server.close()          
            connect_client.close()  
            print("Close Server")
            print('Disconnect Client')
            break

    
CreateServer()