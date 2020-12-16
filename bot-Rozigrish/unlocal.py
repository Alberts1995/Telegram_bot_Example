#import sqlite3
import pymysql.cursors
import time
import datetime
import requests
from pymysql.constants import CLIENT

#DELETE FROM prank WHERE id = (SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1)

class MysqlManager(object):
    def __init__(self):
        self.connect()
    def connect(self):
        try:
            self.connection = pymysql.connect(host='127.0.0.1',
                                                      port=888,
                                                      user='user',
                                                      password='password',
                                                      db='db', 
                                                      autocommit=True, 
                                                      client_flag = CLIENT.MULTI_STATEMENTS)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("WARNING\n", e)
            time.sleep(5)
            self.connect()

    # def inser_chat_id(self, chat_id, text_prank, text_viner, time, message_id, status, chat_name, viner, button, user_id):
    #     sql = """INSERT INTO prank (chat_id, text_prank, text_viner, time, message_id, status, chat_name, viner, button, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    #     values = (chat_id, text_prank, text_viner, time, message_id, status, chat_name, viner, button, user_id)
    #     self.cursor.execute(sql, values)
        

    def insert_new(self, chat_id, chat_name, user_id):
        sql = """INSERT INTO prank (chat_id, chat_name, status, user_id) VALUES (%s, %s, %s, %s)"""
        values = (chat_id, chat_name, 2, user_id)
        self.cursor.execute(sql, values)
        

    def insert_new_user(self, chat_id, first_name):
        sql = """INSERT INTO user (chat_id, first_name) VALUES (?, ?)"""
        values = (chat_id, first_name)
        self.cursor.execute(sql, values)
        

    def select_user(self):
        sql = """SELECT chat_id From user"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i[0] for i in rows]
        return row



    def inser_status_message_id(self, message_id, user_id):
        sql = f"""UPDATE  prank  SET status = 1, message_id = '{message_id}' WHERE user_id = {user_id} AND status = 2 """ #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
        self.cursor.execute(sql)
        

    def inser_text_key(self, button, user_id):
        sql = f"""UPDATE  prank  SET button = '{button}' WHERE user_id = {user_id} AND status = 2""" #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
        self.cursor.execute(sql)
        

    def new_viner(self, viner, user_id):
        sql = f"""UPDATE  prank  SET viner = '{viner}' WHERE user_id = {user_id} AND status = 2""" #=(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) 
        self.cursor.execute(sql)
        


    def inser_text(self, text_prank, time, user_id):
        sql = f"""UPDATE  prank  SET text_prank = '{text_prank}', time = '{time}', button = "Участвовать", 
                viner = "определиться случайно", text_viner = "Победитель" WHERE user_id = {user_id} AND status = 2""" #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) 
        self.cursor.execute(sql)
        

    def update_chanal(self, chat_name, chat_id, user_id):
        for x, y in chat_id.items():
            if x == chat_name:
                sql = f"""UPDATE  prank  SET chat_id = '{y}', chat_name = '{x}' , user_id = '{user_id}', status = 2 WHERE chat_id = '{y}' """ #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
                self.cursor.execute(sql)
        

    def new_text_viner(self, text_viner, user_id):
        sql = f"""UPDATE  prank  SET text_viner = '{text_viner}'  WHERE user_id = {user_id} AND status = 2""" #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
        self.cursor.execute(sql)
        

    def update_text(self, text_prank, user_id):
        sql = f"""UPDATE  prank  SET text_prank = '{text_prank}' WHERE user_id = {user_id} AND status = 2 """ #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
        self.cursor.execute(sql)
        

    def update_data(self, time, user_id):
        sql = f"""UPDATE  prank  SET time = '{time}' WHERE user_id = {user_id} AND status = 2""" # (SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
        self.cursor.execute(sql)
        

    def get_chnal_and_text(self, user_id):
        sql = f""" Select * FROM prank WHERE user_id = {user_id}  AND status = 2 """ #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1)"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows]
        return row

    def get_chnal_and_text_new(self, message_id):
        sql = f""" Select * FROM prank WHERE message_id = '{message_id}'  AND status = 1 """ #(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1)"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows]
        return row

    def get_chnal(self):
        sql = """ Select * FROM prank WHERE status = 0 """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = {f'{i} - {y[7]}':y[1] for i, y in enumerate(rows, 1)}
        return row



    def get_chnal_two(self):
        sql = """ Select * FROM prank WHERE status = 0"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = {y[7]:y[1] for y in rows}
        return row


    def get_chnal_three(self):
        sql = """ Select * FROM prank WHERE status = 2"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = {y[-1]:y[1] for y in rows}
        return row


    def get_time(self):
        sql = """ Select * FROM prank """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows]
        return row


    def get_info(self, user_id):
        sql = f"""Select * FROM prank WHERE user_id = {user_id} AND status = 2 """#(SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows] 
        return row
        

    def delet_informations(self, user_id):
        sql = f"""DELETE FROM prank WHERE user_id = {user_id}  AND status= 2 """# (SELECT * FROM (SELECT id FROM prank ORDER BY id DESC LIMIT 1) AS t1) """
        self.cursor.execute(sql)
        


    def inser_user_new_draw(self, chat_id, user_name, message_id, chanal_id):
        sql = """INSERT INTO user_draw (chat_id, user_name, message_id, chanal_id, status) VALUES (%s, %s, %s, %s, %s)"""
        values = (chat_id, '@' + user_name, message_id, chanal_id, 1)
        self.cursor.execute(sql, values)
        



    def select_info(self, chanal_id):
        sql = f"""Select chat_id, user_name, message_id, chanal_id FROM user_draw WHERE chanal_id = {chanal_id}"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows] 
        if not (row):
            return 0
        else:
            return row


    def select_info_viner(self):
        sql = """Select * FROM user_draw """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows] 
        if row == []:
            return 0
        else:
            return row
    
    def delet_draw(self, message_id):
        sql = f"""DELETE FROM user_draw WHERE message_id = '{message_id}' """
        self.cursor.execute(sql)
        

    def new_update_chanal(self, chat_name, user_id):
        sql = f"""UPDATE  prank  SET status = 2, user_id = {user_id}  WHERE chat_name = '{chat_name}' """
        self.cursor.execute(sql)
        
    

    def inser_status(self, message_id):
        sql = f"""UPDATE  prank  SET status = 0 WHERE message_id = '{message_id}' """
        self.cursor.execute(sql)

    def inser_status_new(self, chat_id):
        sql = f"""UPDATE  prank  SET status = 0 WHERE chat_id = '{chat_id}' """
        self.cursor.execute(sql)

    def act_task(self):
        sql = """SELECT * FROM prank WHERE status = 1"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        row = [i for i in rows]
        return row

        

# if __name__ == "__main__":
#     MysqlManager().select_info_viner()