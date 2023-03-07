import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(empId, name, resumeFile):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        create_query = f" CREATE TABLE IF NOT EXISTS new_employee (id INTEGER PRIMARY KEY,name VARCHAR,resume BLOB NOT NULL)"
        print(create_query)
        cursor.execute(create_query)
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO new_employee
                                  (id, name, resume) VALUES (?, ?, ?)"""

       
        resume = convertToBinaryData(resumeFile)
        # Convert data into tuple format
        data_tuple = (empId, name, resume)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


def writeTofile(data, filename):
            # Convert binary data to proper format and write it on Hard Disk
            with open(filename, 'wb') as file:
                file.write(data)
            print("Stored blob data into: ", filename, "\n")

def readBlobData(empId):
            try:
                sqliteConnection = sqlite3.connect('SQLite_Python.db')
                cursor = sqliteConnection.cursor()
                print("Connected to SQLite")

                sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
                cursor.execute(sql_fetch_blob_query, (empId,))
                record = cursor.fetchall()
                for row in record:
                    print("Id = ", row[0], "Name = ", row[1])
                    name = row[1]                  
                    resumeFile = row[2]

                    print("Storing employee image and resume on disk \n")
                    
                    resumePath = "D:\Courses\\" + name + "_resume.pdf"
                 
                    writeTofile(resumeFile, resumePath)

                cursor.close()

            except sqlite3.Error as error:
                print("Failed to read blob data from sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("sqlite connection is closed")    

if __name__ == "__main__":
    insertBLOB(2, "Smith",  r"C:\Users\chitt\Desktop\JL\instance\uploads\3935c81e-461d-458b-8dfe-b22ed8b343bc_HBNPS9643N_2022-23.pdf")
    readBlobData(2)       