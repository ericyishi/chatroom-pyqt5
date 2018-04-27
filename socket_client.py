# QtGui包含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本。
from PyQt5 import QtGui
from PyQt5.QtGui import QFont  # 设置字体
# QtWidgets模块包含创造经典桌面风格的用户界面提供了一套UI元素的类。
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import sys
import socket
from threading import Thread


class Login(QWidget):  # QWidget类是所有用户界面对象的基类
    def __init__(self):
        QWidget.__init__(self)
        # 设置窗口的位置和大小
        self.setGeometry(600, 300, 400, 300)
        # 设置窗口的标题
        self.setWindowTitle("聊天室")
        # 添加背景
        palette = QtGui.QPalette()
        icon = QtGui.QPixmap(r'./img/1.jpg')
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon))
        self.setPalette(palette)

        self.addUI()
        client = socket.socket()
        client.connect(('127.0.0.1', 9999))
        self.client = client
        self.begin_thread()


        # 创建鼠标点击事件

    def on_click(self):
        print("PyQt5 button click")
        self.send_msg()
        self.text2.clear()

    def addUI(self):  # 添加各种组件

        # 设置多行文本显示框
        self.text = QTextBrowser(self)  # 多行文本框是QTextBrowser
        self.text.setGeometry(30, 30, 300, 100)
        self.text.setStyleSheet('QWidget{background-color:rgb(255,255,255,0%)}')  # 设置输入框透明化

        self.text2 = QLineEdit(self)
        # 设置发送消息
        self.text2.setPlaceholderText(u'发送内容')
        self.text2.setGeometry(30, 160, 300, 30)
        self.text2.setStyleSheet('QWidget{background-color:rgb(255,255,255,0%)}')  # 设置输入框透明化

        # 设置点击按钮
        self.button = QPushButton('发送', self)
        self.button.setFont(QFont('微软雅黑', 10, QFont.Bold))
        self.button.setGeometry(270, 220, 60, 30)
        # self.button = button
        """按钮与鼠标点击事件相关联"""

    def send(self):
        self.button.clicked.connect(self.on_click)

    def begin_thread(self):
        Thread(target=self.send).start()
        Thread(target=self.recv_msg).start()

    def send_msg(self):
        msg = self.text2.text()
        print(msg)
        self.client.send(msg.encode())
        if (msg.upper() == "QUIT"):
            self.client.close()
        self.text2.clear()

    def recv_msg(self):
        while 1:
            try:
                data = self.client.recv(1024).decode()
                data = data + "\n"
                self.text.append(data)
            except:
                exit()

    def closeEvent(self, QCloseEvent):
        self.client.close()

if __name__ == "__main__":
    # 每一pyqt5应用程序必须创建一个应用程序对象。
    app = QApplication(sys.argv)
    dialog = Login()
    # 显示在屏幕上
    dialog.show()
    # 系统exit()方法确保应用程序干净的退出
    sys.exit(app.exec())
