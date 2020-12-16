import sqlite3



class SQLite():
    def __init__(self):
        self.conn = sqlite3.connect("Path", check_same_thread = False)
        self.cursor = self.conn.cursor()

    def inser_chat_id(self, chat_id, text_prank, text_viner, time, message_id, status, chat_name, viner, key):
        sql = """INSERT INTO prank (chat_id, text_prank, text_viner, time, message_id, status, chat_name, viner, key) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (chat_id, text_prank, text_viner, time, message_id, status, chat_name, viner, key)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def insert_new(self, chat_id, chat_name):
        sql = """INSERT INTO prank (chat_id, chat_name, status) VALUES (?, ?, ?)"""
        values = (chat_id, chat_name, 0)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def insert_new_user(self, chat_id, first_name):
        sql = """INSERT INTO user (chat_id, first_name) VALUES (?, ?)"""
        values = (chat_id, first_name)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def select_user(self):
        sql = """SELECT chat_id From user"""
        rows = self.cursor.execute(sql)
        row = [i[0] for i in rows]
        return row

    def inser_status_message_id(self, message_id):
        sql = f"""UPDATE  prank  SET status = 1, message_id = '{message_id}' WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def inser_text_key(self, key):
        sql = f"""UPDATE  prank  SET key = '{key}' WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def new_viner(self, viner):
        sql = f"""UPDATE  prank  SET viner = '{viner}' WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()


    def inser_text(self, text_prank, time):
        sql = f"""UPDATE  prank  SET text_prank = '{text_prank}', time = '{time}', key = "Участвовать", viner = "определиться случайно", text_viner = "Победитель" WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def update_chanal(self, chat_name, chat_id):
        sql = f"""UPDATE  prank  SET chat_id = '{chat_id}', chat_name = '{chat_name}'  WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def new_text_viner(self, text_viner):
        sql = f"""UPDATE  prank  SET text_viner = '{text_viner}'  WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def update_text(self, text_prank):
        sql = f"""UPDATE  prank  SET text_prank = '{text_prank}' WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def update_data(self, time):
        sql = f"""UPDATE  prank  SET time = '{time}' WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()

    def get_chnal_and_text(self):
        sql = """ Select * FROM prank WHERE id = (SELECT id FROM prank ORDER BY id DESC LIMIT 1)"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row

    def get_chnal(self):
        sql = """ Select * FROM prank WHERE status = 0 """
        rows = self.cursor.execute(sql)
        row = {f'{i} - {y[7]}':y[1] for i, y in enumerate(rows, 1)}
        return row


    def get_chnal_two(self):
        sql = """ Select * FROM prank WHERE status = 0"""
        rows = self.cursor.execute(sql)
        row = {y[7]:y[1] for y in rows}
        return row

    def get_time(self):
        sql = """ Select * FROM prank """
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row

    def get_info(self):
        sql = """Select * FROM prank WHERE id =(SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        rows = self.cursor.execute(sql)
        row = [i for i in rows] 
        print(row)
        return row
        

    def delet_informations(self):
        sql = """DELETE FROM prank WHERE id = (SELECT id FROM prank ORDER BY id DESC LIMIT 1) """
        self.cursor.execute(sql)
        self.conn.commit()


    def inser_user_new_draw(self, chat_id, user_name, message_id, chanal_id):
        sql = """INSERT INTO user_draw (chat_id, user_name, message_id, chanal_id, status) VALUES (?, ?, ?, ?, ?)"""
        values = (chat_id, '@' + user_name, message_id, chanal_id, 1)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def select_info(self, chanal_id):
        sql = f"""Select chat_id, user_name, message_id, chanal_id FROM user_draw WHERE chanal_id = {chanal_id}"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows] 
        if row == []:
            return 0
        else:
            return row


    def select_info_viner(self):
        sql = """Select * FROM user_draw """
        rows = self.cursor.execute(sql)
        row = [i for i in rows] 
        if row == []:
            return 0
        else:
            return row
    
    def delet_draw(self, message_id):
        sql = f"""DELETE FROM user_draw WHERE message_id = '{message_id}' """
        self.cursor.execute(sql)
        self.conn.commit()

    def delet_chanal(self, id):
        sql = f"""DELETE FROM prank WHERE id = {id} """
        self.cursor.execute(sql)
        self.conn.commit()
    

    def inser_status(self, message_id):
        sql = f"""UPDATE  prank  SET status = 0 WHERE message_id = '{message_id}' """
        self.cursor.execute(sql)
        self.conn.commit()

    def act_task(self):
        sql = """SELECT * FROM prank WHERE status = 1"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row

    def sel(self, chat_id):
        sql = f"""SELECT * FROM prank WHERE chat_id = {chat_id}"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row
        

if __name__ == "__main__":
    SQLite().get_info()