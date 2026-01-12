import sqlite3
import os
import pandas as pd
from mvc import Model


class DatabaseManager(Model):

    def __init__(self, database="filewatch.db"):


        super().__init__()
        self.__conn = None
        self.__database = database
        self.__cursor = None

        self.create_table()

    def connect(self):
        """Connect to database"""
        if self.__conn is None:
            self.__conn = sqlite3.connect(self.__database, check_same_thread=False)
            self.__cursor = self.__conn.cursor()

    def create_table(self):
        """Create the database table"""
        self.connect()

        self.__cursor.execute("""
                        CREATE TABLE IF NOT EXISTS filewatch (
                                filename TEXT,
                                path TEXT,
                                event_type TEXT,
                                timestamp TEXT )
                                """)

        self.__conn.commit()

    def add_row(self, row):
        """Adds a row to the database"""
        self.connect()
        if self.__conn is None:
            self.__conn = sqlite3.connect(self.__database)
            self.__cursor = self.__conn.cursor()
        query = "INSERT INTO filewatch (filename, path, event_type, timestamp) VALUES (?, ?, ?, ?)"
        filename, path, event_type, timestamp = row

        self.__cursor.execute(query, (filename, path, event_type, timestamp))

        self.__conn.commit()
        self.rows.append(row)

    def query_data(self, extension, event_type, date, t1, t2):
        """Query data from database with provided query data"""
        self.connect()
        query = "SELECT * FROM filewatch WHERE 1=1"
        arg = []

        # Add filters based on the parameters
        if extension:  # If an extension is provided, filter by filename
            query += " AND filename LIKE ?"
            arg.append('%' + extension + '%')

        if event_type:  # If an event type is provided, filter by event_type
            query += " AND event_type LIKE ?"
            arg.append('%' + event_type + '%')

        if date:  # If a date is provided, filter by date
            query += " AND STRFTIME('%F', timestamp) = ?"
            arg.append(date)

        if t1 and t2:  # If both time range values are provided, filter by time
            query += " AND STRFTIME('%T', timestamp) > ? AND STRFTIME('%T', timestamp) < ?"
            arg.append(t1)
            arg.append(t2)

        self.__cursor.execute(query, tuple(arg))

        return self.__cursor.fetchall()


    def write_database(self, export_file, file_name):
        """Write database to a file"""
        self.connect()
        export = os.path.join(export_file, file_name)
        conn = sqlite3.connect(self.__database)
        with open(export, 'w') as f:
            for line in conn.iterdump():
                f.write(line)
                f.write('\n')

    def delete_record(self):
        """Delete all records"""
        self.connect()
        self.__cursor.execute("DELETE FROM filewatch")
        self.__conn.commit()

    def export_db_to_csv(self):
        """Export database to CSV file."""
        self.connect()

        sqlquery = "SELECT * FROM filewatch"


        df = pd.read_sql_query(sqlquery, self.__conn)
        filename = 'filewatch.csv'
        df.to_csv(filename, index=False)
        return filename

    def close(self):
        """Closes the database connection."""
        self.__conn.close()
        self.__cursor.close()
