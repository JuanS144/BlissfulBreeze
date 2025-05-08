"""
    The database.py file handle connection to PostgreSQL database
    and insert and retrive funtionality of courses,students,and sections
    tables
"""
import os
import psycopg2
from config import Config

class Database:
    """
        The Database class contains method which handle connection to 
        PostgreSQL database and methods which handle insert and retrive 
        funtionality of courses,students,and sections
        tables
    """
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def __connect(self):
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=5432
            )
            print("Connection successful!")
            return conn
        except Exception as e:
            print(f"Error: {e}")
     # -----------------------------------
    def __reconnect(self):
        try:
            self.close()
        except psycopg2.Error as f:
            pass
        self.__connection = self.__connect()
     # ----------------------------------
    def  db_conn (self):
        return self.__connection
     # ----------------------------------
    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
     # ----------------------------------
    def commit(self):
        self.__connection.commit()
     # ----------------------------------
    def get_cursor(self):
        for i in range(3):
            try:
                return self.__connection.cursor()
            except Exception as e:
                # Might need to reconnect
                self.__reconnect()
     # ----------------------------------
     # -----------------------------------
    def __run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            # pdb.set_trace()
            with open(file_path, 'r') as f:
                for line in f:
                    if line[:2]=='--': continue
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join( statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                # pdb.set_trace()
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []
     # ----------------------------------
    def run_sql_script(self, sql_filename):
        if os.path.exists(sql_filename):
            self.__connect()
            self.__run_file(sql_filename)
            self.close()
        else:
            print('Invalid Path')

    def delete_users_by_username_pattern(self, pattern):
        """
        Deletes users from the 'salon_user' table where the username matches the pattern.
        """
        try:
            with self.__connection.cursor() as cursor:
                query = "DELETE FROM salon_user WHERE user_name ILIKE %s;"
                cursor.execute(query, (pattern,))
                print(f"Deleted users where username LIKE '{pattern}'")
        except Exception as e:
            print(f"Error deleting users: {e}")


db = Database()
# this db object is imported in the app packages and used (in routes) to handle
# user interactions (listing, creating a new item , ...)

if __name__ == '__main__':
    # pdb.set_trace()

    script_dir = os.path.dirname(__file__)

    sql_file_path = os.path.join(script_dir, 'database.sql')

    db.run_sql_script(sql_file_path)