import socket
import threading

def RecvMsg(client):
    while True:
        msg = client.recv(8192)

        if msg:
            file = open('saveimg.jpg', "wb") # file 변수에 open 함수를 사용해서 (wb) write binary 형태의 객체를 할당 ( 새로운 파일을 작성하겠다는 뜻 ) 
            file.write(msg) # write 를 사용하여 파일의 내용을 작성
            file.close() # 위의 새로운 파일을 생성해주는 객체 변수를 close 해줌 


def SendMsg(client):
    while True:
        try:
            send_msg = input()

            if len(send_msg) == 0:
                print("Close Client")
                break

            if send_msg:
                file = open(send_msg, 'rb')
                image_data = file.read(8192)

                client.send(image_data)

                file.close() 
        except:
            client.close()
            break

def ConnectServer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1002))

    while True:
        try:
            recv_thread = threading.Thread(target=RecvMsg, args=(client, ))
            send_thread = threading.Thread(target=SendMsg, args=(client, ))
            
            recv_thread.start()
            send_thread.start()

        except:
            client.close()
            break


ConnectServer()