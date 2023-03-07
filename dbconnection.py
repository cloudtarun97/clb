import sqlite3
class DBConnection:

    def __init__(self,table_name) -> None:
        self.dbname = "studentsinfo.db"
        self.table_name = table_name
        self.conn = sqlite3.connect(self.dbname,check_same_thread=False)
        self.c = self.conn.cursor()
        create_query = f" CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,RollNo VARCHAR,Name VARCHAR,stream VARCHAR,semester VARCHAR,guide VARCHAR,title VARCHAR,domain VARCHAR,year VARCHAR,file BLOB NOT NULL,desc VARCHAR,resumeFileName VARCHAR)"
        print(create_query)
        self.create_table(create_query)

    def create_table(self,query):
        self.c.execute(query)
        self.conn.commit()


    def insert_query(self,values):
        # print(values)
        query = f"insert into {self.table_name} (RollNo,Name,stream,semester,guide,title,domain,year,file,desc,resumeFileName) values (?,?,?,?,?,?,?,?,?,?,?)"
        print(query)
        self.c.execute(query,values)
        self.conn.commit()

    def select_query(self,condition=None,column_name='*'):

        query = f"select {column_name} from {self.table_name} " if condition is None else f'select {column_name} from {self.table_name} {condition}'
        print(query)
        a=self.c.execute(query)
        print(a.description)
        return a.fetchall()

    def convertToBinaryData(self,filename):
    # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    
    def writeTofile(data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    

    


if __name__ == "__main__":
    # create_column_name = '''RollNo VARCHAR PRIMARY KEY,Name VARCHAR,stream VARCHAR,semester VARCHAR,guide VARCHAR,title VARCHAR,domain VARCHAR,year VARCHAR,file VARCHAR,desc VARCHAR'''
    dbconn = DBConnection("student")
    # res = dbconn.select_query(condition="where stream='mca'")
    # print(res)
    # res = dbconn.select_query(condition="where semester = 'mca'")
    
    # print(res)
    # exit()
    # query = "drop table Shows"
    # dbconn.conn.execute(query)
    # exit()
    # dbconn.c.execute('''CREATE TABLE IF NOT EXISTS Shows
    #           (RollNo VARCHAR PRIMARY KEY,Name VARCHAR,stream VARCHAR,semester VARCHAR,guide VARCHAR,title VARCHAR,domain VARCHAR,year VARCHAR,file VARCHAR,desc VARCHAR)''')
    # dbconn.conn.commit()
    # a=dbconn.c.execute("select * from shows")
    # print(a.description)
    # dbconn.c.execute("insert into shows (RollNo,Name,stream,semester,guide,title,domain,year,file,desc) values ('20VV1F0017','s ch tarun taj','MCA','II-2','JAYA SUMA','PREDECTING','python','2020-2022','','this a new intoduction of')")
    # dbconn.conn.commit()
    # a=dbconn.c.execute("select * from shows")
    # print(a.fetchall())
    query = "drop table student"
    dbconn.conn.execute(query)

    # res=dbconn.select_query()
    # print(res)
    # res1 = dbconn.c.execute("")
    # res1=dbconn.c.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_name = 'students'")
    # print(res1)
    # column_name = 'RollNo,Name,stream,semester,guide,title,domain,year,file,desc'
    # values=('20VV1F0017','s ch tarun taj','MCA','II-2','JAYA SUMA','PREDECTING','python','2020-2022','','this a new intoduction of')
    # dbconn.insert_query(values)
    # res=dbconn.select_query()
    # print(res)

