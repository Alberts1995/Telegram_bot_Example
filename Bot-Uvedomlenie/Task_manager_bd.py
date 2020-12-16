import sqlite3



class SQLite():
    def __init__(self):
        self.conn = sqlite3.connect("Path", check_same_thread = False)
        self.cursor = self.conn.cursor()

    def chat_id_and_status(self, task_date, name_manager, chat_id):
        sql = """INSERT INTO Task_manager_bot (status, task_date, name_manager, chat_id) VALUES (?, ?, ?, ?)"""
        values = (0, task_date, name_manager, chat_id)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def new_task(self, task):
        sql = f"""UPDATE Task_manager_bot SET task = '{task}' WHERE id=(SELECT id FROM Task_manager_bot ORDER BY id DESC LIMIT 1)"""
        self.cursor.execute(sql)
        self.conn.commit()
    
    def select_all(self):
        sql = """SELECT *  FROM Task_manager_bot WHERE id = (SELECT id FROM Task_manager_bot ORDER BY id DESC LIMIT 1)"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row[0]
    
    def select_manager(self, chat_id):
        sql = f"""SELECT *  FROM Task_manager_bot WHERE chat_id = '{chat_id}' AND status = 1"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row

    def select_manager_task_all(self):
        sql = f"""SELECT *  FROM Task_manager_bot """
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row

    def select_all_for_asinck_bot(self):
        sql = f"""SELECT chat_id, task, sleep  FROM Task_manager_bot WHERE status = 1"""
        rows = self.cursor.execute(sql)
        row = [i for i in rows]
        return row
    
    def select_for_buttom(self):
        sql = f"""SELECT name_manager, chat_id FROM Task_manager_bot """
        rows = self.cursor.execute(sql)
        row = {i[0]: i[1] for i in rows}
        return row

    def sleep(self, sleep):
        sql = f"""UPDATE Task_manager_bot SET sleep = "{sleep}", status = 1 WHERE id=(SELECT id FROM Task_manager_bot ORDER BY id DESC LIMIT 1)"""
        self.cursor.execute(sql)
        self.conn.commit()

    def deactivate(self):
        sql = """DELETE FROM 'Task_manager_bot' WHERE id = (SELECT id FROM 'Task_manager_bot' ORDER BY id DESC LIMIT 1)"""
        self.cursor.execute(sql)
        self.conn.commit()

    def deactivate_managers(self, name_manager):
        sql = f"""DELETE FROM Task_manager_bot WHERE name_manager = '{name_manager}'"""
        self.cursor.execute(sql)
        self.conn.commit()

    def deactivate_task(self, task):
        sql = f"""UPDATE Task_manager_bot SET status = 0 WHERE id = {task} """
        self.cursor.execute(sql)
        self.conn.commit()
    
    def update_manager(self, id, name, chat_id):
        sql = f"""UPDATE Task_manager_bot SET name_manager = '{name}', chat_id = {chat_id} WHERE id = {id}"""
        self.cursor.execute(sql)
        self.conn.commit()

    def update_sleep(self, sleep, task):
        sql = f"""UPDATE Task_manager_bot SET sleep = '{sleep}' WHERE id = {task}"""
        self.cursor.execute(sql)
        self.conn.commit()

    def update_task(self, id, task):
        sql = f"""UPDATE Task_manager_bot SET task = '{task}' WHERE id = {id}"""
        self.cursor.execute(sql)
        self.conn.commit()

    def new_manager(self, name_manager, chat_id):
        sql = f"""INSERT INTO Task_manager_bot (chat_id ,name_manager) VALUES (?, ?)"""
        values = (chat_id, name_manager)
        self.cursor.execute(sql, values)
        self.conn.commit()


    
