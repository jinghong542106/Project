from socket import *

sockfd=socket(AF_INET,SOCK_STREAM)

sockfd.connect(("127.0.0.1",8888))
while True:

    data=input("发送>>")
    if data=="##":
        break
    n=sockfd.send(data.encode())
   
    data=sockfd.recv(1024)
    print("received data:",data.decode())


sockfd.close()