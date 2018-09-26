from socket import *
import sys
import os
import time


# 基本文件操作功能
class FtpClient(object):
    """docstring for FtpClient"""
    def __init__(self, sockfd):
        self.sockfd = sockfd
    def do_list(self):
        self.sockfd.send(b"L") #发送请求
        data=self.sockfd.recv(1024).decode()
        # print(data)
        if data=="OK":
            data=self.sockfd.recv(4096).decode()
            files=data.split("#")
            for file in files:
                print(file)
            print("文件展示完毕\n")
        else:
            # 服务器发送失败通知
            print("失败原因:",data)

    def do_get(self,filename): 
        self.sockfd.send(("G "+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data=="OK":
            f=open(filename,"wb")
            while True:
                data=self.sockfd.recv(1024)
                if data==b"##":
                    break
                f.write(data)
            f.close()
            print("%s下载完毕\n" % filename)       
        else:
            # 服务器发送失败通知
            print("失败原因:",data)

    def do_quit(self):
        self.sockfd.send(b"Q")

    def do_put(self,filename):
        self.sockfd.send(("P "+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data=="OK":
            try:
                f=open("./"+filename,"rb")
            except Exception as e:
                print("错误类型:", e)
            while True:
                data=f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b"##")
                    break
                self.sockfd.send(data)
            f.close()
        else:
            # 服务器发送失败通知
            print("失败原因:",data)

def main():
    if len(sys.argv)<3:
        print("agrv is error")
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)

    sockfd=socket(AF_INET,SOCK_STREAM)
    try:
        sockfd.connect(ADDR)
    except :
        print("连接服务器失败")
        return
    fc=FtpClient(sockfd) #功能类对象

    while True:
        print("*******list**********")
        print("******* get *********")
        print("******* put *********")
        print("*******quit *********")

        cmd=input("发送>>")
        if cmd.strip()=="list":
            fc.do_list()
        elif cmd[:3]=="get":
            filename=cmd.split()[-1]
            fc.do_get(filename)
        elif cmd[:3]=="put":
            put_filename=cmd.split()[-1]
            fc.do_put(put_filename)
            pass
        elif cmd.strip()=="quit":
            fc.do_quit()
            sockfd.close()
            sys.exit("谢谢使用")
        else:
            print("请输入正确的命令")
            continue
     
    sockfd.close()
if __name__=="__main__":
    main()
