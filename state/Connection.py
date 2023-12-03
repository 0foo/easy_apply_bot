import sqlite3

"""
Meta and utility methods for building database models. 
Sqllite3 right now but will abstract out at some point

"""

class Connection:
    con = None

    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
    
    def __del__(self):
        self.con.close()

    def close_connection(self):
        self.con.close()
        
    def fetch_all(self, command):
        cursor = self.con.cursor()
        cursor.execute(command)
        results = cursor.fetchall()
        cursor.close()
        return results
    

    def get_new_cursor(self):
        cursor = self.con.cursor()
        return cursor.fetch()

    def item_exists(self, command):
        cursor = self.con.cursor()
        cursor.execute(command)
        count = cursor.fetchone()[0]
        cursor.close()
        if count > 0: 
            return True
        return False

    def execute(self, command):
        with self.con:
            self.con.execute(command)
        return True
    
    def row_count(self, table_name):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        cursor.close()
        return row_count
    
    def table_exists(self, table_name):
        cursor = self.con.cursor()
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        cursor.execute(query, (table_name,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    
    def fetch_col_as_list(self, col_num, command):
        result = self.fetch_all(command)
        result = [row[col_num] for row in result]
        if result:
            return result
        return []

