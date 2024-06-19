import mysql.connector
from mysql.connector import Error


class MySQLConnector:
    def __init__(self,
                 host="127.0.0.1",
                 username="root",
                 password="1234",
                 database="water"):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
        except mysql.connector.errors.ProgrammingError as e:
            print("Произошла ошибка программирования:", e)
            conn = None
        except Error as e:
            print("Произошла ошибка базы данных:", e)
            conn = None
        return conn

    def execute(self, query, value_to_insert=None):
        conn = self.connect()
        if conn is not None:
            cursor = conn.cursor()
            if value_to_insert is None:
                cursor.execute(query)
            else:
                cursor.execute(query, value_to_insert)
                conn.commit()
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        return None
