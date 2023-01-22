import socket
import threading

def RecvMsg(connect_client, connect_client_address):
    while True:
        msg = connect_client.recv(8192)

        if msg:
            file = open(str(connect_client_address) +'.jpg', "wb") # file 변수에 open 함수를 사용해서 (wb) write binary 형태의 객체를 할당 ( 새로운 파일을 작성하겠다는 뜻 ) 
            file.write(msg) # write 를 사용하여 파일의 내용을 작성
            file.close() # 위의 새로운 파일을 생성해주는 객체 변수를 close 해줌 

                
     

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

            recv_thread = threading.Thread(target=RecvMsg, args=(connect_client, connect_client_address))
            send_thread = threading.Thread(target=SendMsg, args=(connect_client, server))

            recv_thread.start()
            send_thread.start()
        except:
            server.close()          
            connect_client.close()  
            print("Close Server")
            print('Disconnect Client')
            break

    
CreateServer()