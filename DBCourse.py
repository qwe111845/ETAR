# -*- coding: utf-8 -*-
import threading
import MySQLdb
import functools
import time
import json


def synchronized(wrapped):
    lock = threading.Lock()
    print(lock, id(lock))

    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            print("Calling '%s' with Lock %s from thread %s [%s]"
                  % (wrapped.__name__, id(lock),
                     threading.current_thread().name, time.time()))
            result = wrapped(*args, **kwargs)
            print("Done '%s' with Lock %s from thread %s [%s]\n"
                  % (wrapped.__name__, id(lock),
                     threading.current_thread().name, time.time()))
            return result

    return _wrap


class DBCourse:

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "user", "1234", "student", charset='utf8')
        self.cursor = self.db.cursor()

    def get_class(self):
        self.cursor.execute("select course_name from course_information;")
        results = self.cursor.fetchall()
        class_names = ''
        for i in results:
            class_names += i[0] + ';'

        return class_names

    def get_course_name(self, course):
        course_data = course.split(',')

        sql = "SELECT course_name FROM course_information WHERE course_teacher = '{}' " \
              "and course_dayofweek = {} and course_starthour <= {} and course_endhour >= {}" \
            .format(course_data[0], course_data[1], course_data[2], course_data[2])
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        results = self.cursor.fetchone()

        if results is not None:
            return results[0]
        else:
            return '目前沒有課程'

    def get_student_data(self, course):
        students = ''
        print(course)

        print('連接mysql')
        course_id = str(self.get_course_id(course))
        print(course_id)
        sql = "SELECT student_id,student_name FROM student_data ,practice_courses as p " + \
              "WHERE student_id = p.stu_id and course_id = {};".format(course_id)

        try:
            self.cursor.execute(sql)
        except NameError:
            print("連線失敗", self.db.rollback())
        except TypeError:
            print('型態錯誤')
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        results = self.cursor.fetchall()
        for i in results:
            students += i[0] + ' ' + i[1] + ';'

        return students

    @synchronized
    def roll_call(self, data, course):

        date = 'curdate()'
        attends = data[:-1]
        attends = attends.split(';')
        sql_sentence = ''
        course_id = self.get_course_id(course)
        for rollcall in attends:
            rollcall = rollcall.split()
            sql_sentence += "('{}','{}','{}','{}', {}),".format(rollcall[0], rollcall[1], course_id, rollcall[2], date)

        sql_sentence = sql_sentence[:-1]
        sql_sentence = "INSERT INTO roll_call(stu_id, stu_name, course_id , status, datetime) VALUES {};" \
            .format(sql_sentence)
        try:
            self.cursor.execute(sql_sentence)
            self.db.commit()
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql_sentence)
            self.db.commit()

        return True

    def get_course_id(self, course):

        sql = "SELECT course_id FROM student.course_information " + \
              "WHERE course_name = \"{}\";".format(course)

        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        results = self.cursor.fetchone()

        return results[0]

    def get_teacher_account(self, account):

        sql = "SELECT lesson_id, lesson, title, teacher_name FROM course_3565.lesson as c, student.teacher_data as t " \
              "WHERE c.lesson_id = (SELECT current_course FROM student.course_progress WHERE sid = \"{}\") " \
              "and teacher_id = \"{}\";".format(account, account)
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
        results = self.cursor.fetchone()

        teacher_data = {}

        if len(results) == 0:
            return 'no account'
        else:
            teacher_data['lesson_id'] = results[0]
            teacher_data['lesson'] = results[1]
            teacher_data['title'] = results[2]
            teacher_data['teacher_name'] = results[3]
            print json.dumps(teacher_data)
            return json.dumps(teacher_data)

    def get_word(self, lesson):

        sql = "SELECT word FROM course_3565.words WHERE lesson = (SELECT lesson FROM course_3565.lesson WHERE" + \
              " lesson = {});".format(str(lesson))
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        words = {'words': []}
        results = self.cursor.fetchall()
        for res in results:
            words['words'].append(res[0])

        return json.dumps(words)

    def get_quiz(self, unit):

        import json
        sql = "SELECT q.`order`, q.answer, q.quiz, a.content FROM course_3565.lesson_quiz AS q," \
              "course_3565.lesson_answer AS a WHERE	q.lesson = {} AND a.lesson = {}	AND " \
              "a.`q_order` = q.`order`  AND q.answer = a.answer;".format(str(unit), str(unit))

        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        order = []
        answer = []
        quizes = []
        content = []

        quiz = {'order': [], 'answer': [], 'quiz': [], 'content': []}
        results = self.cursor.fetchall()

        for res in results:
            order.append(res[0])
            answer.append(res[1])
            quizes.append(res[2])
            content.append(res[3])

        quiz['order'] = order
        quiz['answer'] = answer
        quiz['quiz'] = quizes
        quiz['content'] = content

        return json.dumps(quiz)

    def update_progress(self, data):
        stu_data = data.split(';')
        student = stu_data[0]
        course = stu_data[1]

        sql = "UPDATE student.course_progress SET current_course = {} WHERE sid = \"{}\";".format(course, student)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
            self.db.commit()

    def operation_error(self):
        self.db = MySQLdb.connect("127.0.0.1", "user", "1234", "student", charset='utf8')
        self.cursor = self.db.cursor()
        print('reconnect database')
