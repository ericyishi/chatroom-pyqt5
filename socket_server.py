import socket
from threading import Thread

import time


class server:
    def __init__(self):
        server = socket.socket()
        server.bind(('127.0.0.1', 9999))
        server.listen(5)
        self.server = server
        self.li = []  # # 是客户端对象的列表
        self.di = {}  # 添加用户名和ip地址
        self.get_con()

    def get_con(self):  # 循环的等待客户端的连接，成功返回连接成功
        while 1:
            con, addr = self.server.accept()
            data = '连接成功!,请输入昵称'
            con.send(data.encode())  # 通知已经链接进来的的客户端
            Thread(target=self.get_msg, args=(con, self.li, self.di, addr)).start()  # 启动子线程
            self.li.append(con)  # 添加已经连接的客户端对象到列表，方便群发消息

    def get_msg(self, con, li, di, addr):
        name = con.recv(1024).decode()  # 接收客户端发来的昵称
        # print("用户输入的name:%s"%name)
        di[addr] = name  # 向字典里添加当前的昵称并和addr对应
        while 1:  # 循环监听客户端的消息
            try:
                redata = con.recv(1024).decode()
                # print("收到内容是%s" % redata)
            except Exception as e:
                # print("提示::", e)
                self.close_client(con, addr)
                break;
            if (redata.upper() == "QUIT"):
                self.close_client(con, addr)
                break;
            # 只有接收到recv后才会执行下面的操作
            print(di[addr] + ' ' + time.strftime('%x') + ':\n' + redata)
            for i in li:  # 广播在客户列表里的成员，每一个人都要发送一遍
                # 通过字典查询，得到当前发送消息的客户端名称，并和消息连接
                i.send((di[addr] + ' ' + time.strftime('%x') + ':\n' + redata).encode())

    def close_client(self, con, addr):
        self.li.remove(con)
        # print("client:", self.li)
        con.close()
        print(self.di[addr] + "已经离开了")
        for k in self.li:
            k.send((self.di[addr] + "已经离开了").encode())


if __name__ == "__main__":
    server()
