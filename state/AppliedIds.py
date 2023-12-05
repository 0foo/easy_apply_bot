from Connection import Connection

class AppliedIds:
    
    con = None
    easy_db='./easy_apply.db'

    def __init__(self):
        if not self.con:    
            self.con = Connection(self.easy_db)
            
        if not self.con.table_exists("AppliedIds"):
            self.create_applied_ids_table()

    def create_applied_ids_table(self):
        self.con.execute(
            """
                CREATE TABLE AppliedIds (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    applied_id INTEGER UNIQUE 
                );
            """
        )
        self.con.execute(""" 
            CREATE INDEX applied_id_index ON AppliedIds (applied_id);
        """)

    def fetch_all(self):
        return self.con.fetch_col_as_list(0, "SELECT applied_id from AppliedIds")

    def add(self, applied_id):
        try:
            self.con.execute(f"INSERT INTO AppliedIds (applied_id) VALUES ({applied_id})")
        except:
            return False
        return True

    def delete(self, applied_id):
        self.con.execute(f"DELETE FROM AppliedIds WHERE applied_id = {applied_id};")

    def total(self):
        return self.con.row_count("AppliedIds")
    
    def item_exists(self, applied_id):
        return self.con.item_exists(f"SELECT COUNT(*) FROM AppliedIds WHERE applied_id = {applied_id}")