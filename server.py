# -*- coding: utf-8 -*-

import socket
import threading
import time

import DBCourse


class Server:
    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.dbc = DBCourse.DBCourse()
        self.course = ''
        self.results = ''
        self.robot_port = 5400

    def listen(self):

        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(300)
            threading.Thread(args=(client, address), target=self.listen_to_client).start()

    def listen_to_client(self, client, address):

        print('connect by: ', address)

        size = 2048
        link = True  # type: bool
        while link:
            try:
                data = client.recv(size)
                if data:
                    print(data.decode('utf-8'))

                    if data == 'teacher account':
                        client.send('account')
                        teacher_account = client.recv(1024)
                        result = self.dbc.get_teacher_account(teacher_account)
                        client.send(result)
                        link = False

                    elif data == '點名':
                        client.send('接收點名')
                        roll_call_course = client.recv(size)

                        self.course = roll_call_course.strip()
                        all_students = self.dbc.get_student_data(self.course)

                        while all_students == '':
                            time.sleep(1)
                            all_students = self.dbc.get_student_data(self.course)

                            print ('重新存取資料')

                        stu_names = str(all_students.encode('utf-8'))
                        client.send(stu_names)

                        print('傳送' + stu_names)
                        link = False

                    elif data == '點名完畢':
                        client.send('接收成功')
                        roll_call_data = client.recv(size)
                        record_success = self.dbc.roll_call(roll_call_data, self.course)

                        if record_success:
                            print(roll_call_data, '出席紀錄成功')
                        link = False

                    elif data == '所有課程':
                        class_names = self.dbc.get_class().encode('utf-8')
                        client.send(class_names)

                        print('課程:', class_names.decode('utf-8'))
                        link = False

                    elif data == '找課程':
                        client.send('ok')
                        course_name = client.recv(size)
                        if len(self.dbc.get_course_name(course_name)) > 0:
                            if isinstance(self.dbc.get_course_name(course_name), unicode):
                                response = self.dbc.get_course_name(course_name).encode('utf-8')
                            else:
                                response = self.dbc.get_course_name(course_name)
                        else:
                            response = '沒有課程'
                        client.send(response)
                        link = False

                    elif data == 'word_course':
                        client.send('Which unit do you want to choose?')
                        word_unit = client.recv(size)
                        word_data = self.dbc.get_word(word_unit)
                        time.sleep(0.5)
                        client.sendall(word_data)
                        link = False

                    elif data == 'quiz_course':
                        client.send('Which unit do you want to choose?')
                        quiz_unit = client.recv(size)
                        quiz_data = self.dbc.get_quiz(quiz_unit)
                        print(quiz_data)
                        time.sleep(0.5)
                        client.sendall(quiz_data)
                        link = False

                    elif data == 'get robot port':
                        print(self.robot_port)
                        client.send(str(self.robot_port))
                        link = False

                    elif data == 'get robot port(G)':
                        client.send(str(self.robot_port))
                        link = False

                    elif data == 'add port':
                        self.robot_port += 1
                        if self.robot_port >= 5500:
                            self.robot_port = 5400
                        link = False

                    elif data == 'update progress course':
                        client.send('ok')
                        student_data = client.recv(1024)
                        progress = self.dbc.update_progress(student_data)
                        client.send(progress)
                        link = False

                    elif data == 'wer':
                        from word_error_rate import wer_improve
                        client.send('ok')
                        student_say = client.recv(1024).split(';;')
                        wer = str(int((1 - wer_improve.wer(student_say[0], student_say[1])) * 100))
                        client.send(wer)

                    else:
                        print(type(data), '傳送', data.decode('utf-8'))
                        client.sendall(data.decode('utf-8'))

                else:
                    time.sleep(1)
            except TypeError:
                client.close()
                return False

        client.close()


Server('140.134.26.200', 5007).listen()
