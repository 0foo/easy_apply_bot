from .Connection import Connection

class JobIds:
    
    con = None
    easy_db='./easy_apply.db'

    def __init__(self):
        self.con = Connection(self.easy_db)
        if not self.con.table_exists("JobIds"):
            self.create_job_ids_table()

    def create_job_ids_table(self):
        self.con.execute(
            """
                CREATE TABLE JobIds (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    job_id INTEGER,
                    search_term TEXT,
                    UNIQUE(job_id, search_term)
                );
            """
        )
        self.con.execute(""" 
            CREATE INDEX job_id_index ON JobIds (job_id);
        """)

    def add(self, job_id, search_term):
        try:
            self.con.execute(f"INSERT INTO JobIds (job_id, search_term) VALUES ({job_id}, '{search_term}');")
        except:
            return False
        return True

    def delete(self, job_id):
        self.con.execute(f"DELETE FROM JobIds WHERE job_id = {job_id};")
    
    def purge(self):
        self.con.execute(f"DELETE from JobIds")
        self.con.execute(f"DELETE FROM sqlite_sequence WHERE name='JobIds';")

    def total(self):
        return self.con.row_count("JobIds")
    
    def exists(self, job_id, search_term):
        return self.con.item_exists(f"SELECT COUNT(*) FROM JobIds WHERE job_id='{job_id}' AND search_term='{search_term}'")
   
    def get_by_keyword(self, keyword):
        job_ids = self.con.fetch_col_as_list(0, f"SELECT job_id FROM JobIds WHERE search_term LIKE ('%{keyword}%')")
        if job_ids:
            return job_ids
        return []
    
    def item_exists(self, job_id):
        return self.con.item_exists(f"SELECT COUNT(*) FROM JobIds WHERE job_id = {job_id}")