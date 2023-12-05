from Connection import Connection

class DeletedIds:
    
    con = None
    easy_db='./easy_apply.db'

    def __init__(self):
        self.con = Connection(self.easy_db)
        if not self.con.table_exists("DeletedIds"):
            self.create_deleted_ids_table()

    def create_deleted_ids_table(self):
        self.con.execute(
            """
                CREATE TABLE DeletedIds (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    deleted_id INTEGER,
                    search_term TEXT,
                    UNIQUE(deleted_id, search_term)
                );
            """
        )
        self.con.execute(""" 
            CREATE INDEX deleted_id_index ON DeletedIds (deleted_id);
        """)

    def fetch_all(self):
        return self.con.fetch_col_as_list(0, "SELECT deleted_id from DeletedIds")

    def add(self, deleted_id, search_term):
        try:
            self.con.execute(f"INSERT INTO DeletedIds (deleted_id, search_term) VALUES ({deleted_id}, '{search_term}')")
        except:
            return False
        return True

    def delete(self, deleted_id):
        self.con.execute(f"DELETE FROM DeletedIds WHERE deleted_id = {deleted_id};")

    def total(self):
        return self.con.row_count("DeletedIds")
    
    def item_exists(self, deleted_id,):
        return self.con.item_exists(f"SELECT COUNT(*) FROM DeletedIds WHERE deleted_id = {deleted_id}")
    
    def exists(self, deleted_id, search_term):
        return self.con.item_exists(f"SELECT COUNT(*) FROM DeletedIds WHERE deleted_id='{deleted_id}' AND search_term='{search_term}'")
   