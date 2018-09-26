# <!-- 使用fork完成并发
# 1. 创建套接字，绑定，监听
# 2. 等待接受客户端连接请求
# 3. 创建新的进程处理客户端请求
#    父进程继续等待连接其他客户端
# 4. 客户端退出 对应子进程结束 

from socket import *
import os,sys
import signal


def client_hander(c):
    print("处理子进程的请求", c.getpeername())
    try:
        while True:
            data=c.recv(1024)
            if not data:
                break
            print(data.decode())
            c.send("收到客户端请求".encode())
    except (KeyboardInterrupt, SyntaxError):
        sys.exit("客户端退出")
    except Exception as e:
        print(e)
    c.close()
    sys.exit("客户端退出")
# 创建套接字，绑定，监听
HOST="0.0.0.0"
PORT=8888
ADDR=(HOST,PORT)
s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

print("进程%d等待客户端连接" % os.getpid())

# 在父进程中忽略子进程状态改变，子进程退出自动由系统出来处理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    try:
        c,addr=s.accept()
    except KeyboardInterrupt:
        sys.exit("服务器退出")
    except Exception as e:
        print("Error", e)
        continue
    # 为客户端创建新的进程来处理请求
    pid=os.fork()
    if pid==0:
        s.close()
        client_hander(c)
        
    # 父进程或者创建失败都继续等待下个客户端链接  
    else:
        c.close()
        continue







