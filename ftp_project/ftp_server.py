from socket import *
import os
import sys
import time
import signal

FILE_PATH = "/home/tarena/aid1807/ftpfile/"
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)


class FtpServer(object):
    """定义服务端的功能处理类，对客户端请求进行处理"""

    def __init__(self, connfd):
        self.connfd = connfd      

    def do_list(self):
        # 获取文件列表
        file_list=os.listdir(FILE_PATH)
        if not file_list:
            self.connfd.send("文件库为空".encode())
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
        files=""
        for file in file_list:
            if file[0]!="." and\
                os.path.isfile(FILE_PATH+file):
                files=files+file+"#"
        self.connfd.send(files.encode())
    def do_get(self,filename):
        try:
            f=open(FILE_PATH+filename,"rb")
        except :
            self.connfd.send("文件不存在".encode())
            return
        self.connfd.send(b"OK")
        time.sleep(0.1)
        while True:
            data=f.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b"##")
                break
            self.connfd.send(data)
        f.close()
    def do_put(self,filename):
        f=open(FILE_PATH+filename,"wb")
        self.connfd.send(b"OK")
        while True:
            data=self.connfd.recv(1024)
            if data==b"##":
                break
            f.write(data)
        f.close()
        print("%s上传完毕\n" % filename)    

def main():
    # 创建套接字，绑定，监听
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print("进程%d等待客户端连接" % os.getpid())
    # 在父进程中忽略子进程状态改变，子进程退出自动由系统出来处理
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            connfd, addr = s.accept()
        except KeyboardInterrupt:
            s.close()
            sys.exit("Ftp服务器退出")
        except Exception as e:
            print("服务器异常:", e)
            continue
        print("已连接客户端:", addr)
        # 为服务端创建新的进程来处理客户端请求
        pid = os.fork()
        if pid == 0:
            s.close()
            fs=FtpServer(connfd)
            # 判断客户端的请求
            while True:
                data=connfd.recv(1024).decode()
                if not data or data[0] == "Q":
                    connfd.close()
                    sys.exit("客户端退出")
                elif data[0]=="L":
                    fs.do_list()
                elif data[0]=="G":
                    filename=data.split()[-1]
                    fs.do_get(filename)
                elif data[0]=="P":
                    filename=data.split()[-1]
                    fs.do_put(filename)

            sys.exit("exit")
        # 父进程或者创建失败都继续等待下个客户端链接
        else:
            connfd.close()
            continue


if __name__ == "__main__":
    main()
