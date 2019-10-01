# -*- coding: utf-8 -*-
import socket
import time
import threading as td


def get_robot_port():
    port = 5007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('140.134.26.200', port))
    s.send('get robot port(G)')
    robot_port = int(s.recv(1024))
    time.sleep(1)
    s.close()
    return robot_port


class PPTClient:
    def __init__(self):
        self.robot_port = 5400
        self.command = ''
        self.ip = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = ''
        self.link = True

    def main(self, ip):
        self.ip = ip
        self.robot_port = get_robot_port()
        self.socket = self.connect(self.ip, self.robot_port)
        #self.socket = self.connect((self.ip, 5408))
        print('連線')

    def connect(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, port))
            self.status = '已連線'
        except socket.error, msg:
            self.status = '連線失敗'
            print(msg)
        return sock

    def quit_ppt(self):
        self.status = '關閉連線'
        port = 5007
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('140.134.26.200', port))
        s.send('add port')
        time.sleep(1)
        s.close()

    def get_status(self):
        return self.status

    def set_command(self, command):
        self.command = command

        try:
            self.socket.send(self.command)
            print("send msg ok : ", self.command)
            self.command = ''
            self.status = '已連接'
        except socket.error:
            print("\r\nsocket error,do reconnect ")
            time.sleep(3)
            self.status = '重新連接'
            self.socket = self.connect(self.ip, self.robot_port)
        except TypeError:
            self.status = '連接失敗'
            print('\r\nother error occur ')
            time.sleep(3)
        if command == 'Quit ppt mode':
            self.quit_ppt()

