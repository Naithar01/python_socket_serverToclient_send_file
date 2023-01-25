import socket
import threading

import datetime


# 클라이언트로부터 send 를 recv 해주는 함수
# 매개변수로 connect에 성공한 클라이언트를 받음

# 20: 연결된 클라이언트로부터 send 받은 내용을 recv 함수를 통해 msg 변수에 넣음 ( recv 함수의 첫 번째 인자에 들어가는 값은 버퍼로 일시적으로 데이터를 보관할 수 있는 메모리 용량 )
# 23: 받은 내용이 존재한다는 if 문을 거쳐 save_file_name 이라는 변수에 현재 시-분-초-날자 등의 값을 넣어줌 ( 새로 저장할 파일의 이름 ) 
# 25: open 함수는 새로운 파일을 저장하거나 혹은 존재하는 파일의 내용을 수정할 때 사용하는 함수인데 새로운 파일을 만들어 write 해줄 것이기 때문에 첫 번째 매개변수로는 ( 파일 이름, 확장자 ), 두 번째 매개변수로는 새로운 파일을 작성할 것이기 때문에 "wb" 그게 아니라면 "rb" ( write, read ) 오픈한 파일을 file 변수에 넣어줌 
# 26: 선언한 변수의 type(BufferedWriter) write method 를 사용하여 파일 내용을 작성
# 28: 작성이 끝나면 close method로 파일을 닫아줌

# 만약 그 과정에서 에러가 생겼다면 연결된 클라이언트의 접속을 끊어버리고 반복문 종료 다시 클라이언트를 accept 받는 곳으로 이동함 
def RecvMsg(connect_client):
    while True:
        try:
            msg = connect_client.recv(8192)

            if msg:
                save_file_name = datetime.datetime.now()

                file = open(str(save_file_name).replace(":", " ") + '.jpg', "wb")
                file.write(msg)

                file.close()
        except:
            connect_client.close()
            break

# 클라이언트에게 send 해주는 함수 

# 무한하게 문자를 주고 받기 위해서 while 반복문을 사용 input 함수로 콘솔에서 입력받은 내용을 send_msg 변수로 선언  
# 48: 만약에 입력한 내용이 없고 엔터를 입력받으면 프로그램 종료
# 53: 파일 내용을 제대로 입력 받으면 open 함수를 사용하여 파일을 열고 file 변수에 선언하는데 파일이 없으면 프로그램 종료 
# 54: image_data 변수에 불러온 이미지의 버퍼값을 선언
# 56: 클라이언트에게 버퍼 값을 보내줌 
# 58: open 함수로 열었던 파일을 close method로 종료 

#
def SendMsg(connect_client, server):
    while True:
        try:
            send_msg = input()

            if len(send_msg) == 0:
                server.close()
                connect_client.close()
                break

            file = open(send_msg, 'rb')
            image_data = file.read(8192)

            connect_client.send(image_data)

            file.close()

        except:
            connect_client.close()
            break


def CreateServer():
    # 새로운 소켓을 만듦
    # AF_INET, SOCK_STREAM 는 socket을 설정할 때 지정해주는 특성 값
    # AF_INET 는 해당 소켓을 IP version 4 로 사용하겠단 의미
    # IP version 4 는 인터넷 프로토콜의 4번째 판이며, 전 세계적으로 사용된 첫 번째 인터넷 프로토콜
    # SOCK_STREAM 는 해당 소켓의 TCP 패킷을 받겠단 의미
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind 함수는 서버측에 특정 port 와 host 이름으로 연결하겠다는 의미
    server.bind(('localhost', 1002))

    # 클라이언트의 연결 요청을 받을 준비가 됐다는 코드
    # 첫 번째 매개변수로 몇 개 까지의 클라이언트를 받을건지 넣을 수 있음
    server.listen()

    print("Server is Running...")

    while True:
        try:
            # 클라이언트의 연결을 받고 
            connect_client, connect_client_address = server.accept()
            # 클라이언트와 연결을 하는데 문제가 없다면 콘솔로 출력 ( 클라이언트 정보 ) 
            print(f"Connect {connect_client_address}")

            # 클라이언트에게 문자를 보냄과 받음을 동시에 하기위해 하나의 동작은 쓰래드로 만들고 각각 매개변수로 (서버), (서버, 클라이언트)를 매개변수로 전달해줌 
            send_thread = threading.Thread(
                target=SendMsg, args=(connect_client, server))

            send_thread.start()
            RecvMsg(connect_client)

        except:
            connect_client.close()
            print('Disconnect Client')
            break


CreateServer()
