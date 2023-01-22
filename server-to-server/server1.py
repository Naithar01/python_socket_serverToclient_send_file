import socket
import sys

import time

def Print_Hellp_Message():
    print("Help Option :: ")
    print("python server1.py -sh [Server Host] -sp [Server Port] -csh [Connect Server Host] -csp [Connect Server Port] ")
    print("Server: -sh: Server Host")
    print("Server: -sp: Server Port")

    print("Connect Server: -csh: Connect Server Host")
    print("Connect Server: -csp: Connect Server Port")

    print("Ex) python server1.py -sh localhost -sp 8001 -csh localhost -csp 8004")

def Setting_Options():
    argvs = sys.argv

    if len(argvs) != 9:
        Print_Hellp_Message()
        
        time.sleep(5)

        sys.exit()

    server_host = argvs[2]
    server_port = argvs[4]
    
    connect_Server_Host = argvs[6]
    connect_Server_Port = argvs[8]

    if len(server_host) == 0 or len(server_port) == 0 or len(connect_Server_Host) == 0 or len(connect_Server_Port) == 0 :
        Print_Hellp_Message()

        time.sleep(5)

        sys.exit()

    if server_port == connect_Server_Port:
        Print_Hellp_Message()

        print("Read: Enter different Port | sp != csp")

        time.sleep(5)

        sys.exit()

    return server_host, server_port, connect_Server_Host, connect_Server_Port

server_host, server_port, connect_Server_Host, connect_Server_Port = Setting_Options()

# acceptServer #  connectServer
# connectServer # acceptServer

class Server:
    def __init__(self, server_host, server_port, connect_Server_Host, connect_Server_Port):
        self.SERVER_HOST = server_host
        self.SERVER_PORT = server_port
        
        self.CONNECT_SERVER_HOST = connect_Server_Host
        self.CONNECT_SERVER_PORT = connect_Server_Port

        self.CreateServer()
        self.AcceptServerAndConnectServer()

    def DisconnectServer(self):
        self.server.close()

        print("Disconnect Server")

    def DisconnectServerAndConnectServer(self):
        self.server.close()
        self.acceptServer.close()
        self.connectServer.close()

        print("Disconnect Server & Disconnect ConnectServer & Disconnect AcceptServer ")

        sys.exit()

    def CreateServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.server.bind((self.SERVER_HOST, int(self.SERVER_PORT))) # TypeError: 'str' object cannot be interpreted as an integer
        self.server.listen()

        print(f"Create Server... host: {self.SERVER_HOST} | port: {self.SERVER_PORT}")

    def AcceptServerAndConnectServer(self):
        print("Connect Waiting...")

        try:
            self.acceptServer, self.acceptServerAddress = self.server.accept()

            self.connectServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connectServer.connect((self.CONNECT_SERVER_HOST, int(self.CONNECT_SERVER_PORT)))

        except:
            print("Connect Error: Connect Fail")
            self.DisconnectServer()
        
        print(f"Connect Success... Connect Server Info: {self.acceptServerAddress}")

        self.SendFile()

    def SendFile(self):
        while True:
            # Print Message

            msg = self.acceptServer.recv(4096)

            if msg == "exit":
                self.DisconnectServerAndConnectServer()

            print(f"Get Msg {msg}")

            # Send Message

            send_text = input()

            if send_text == "exit":
                self.DisconnectServerAndConnectServer()

            self.connectServer.send(send_text)

Server(server_host, server_port, connect_Server_Host, connect_Server_Port)