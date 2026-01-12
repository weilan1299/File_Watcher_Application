import unittest
from unittest.mock import patch, MagicMock
from databasemanager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_create_table(self, mock_connect):
        """Test if database is created correctly."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        row = ('test.txt', '/path/to/file', 'CREATE', '2025-03-20 10:00:00')

        db.add_row(row)

        mock_cursor.execute.assert_any_call("""
                        CREATE TABLE IF NOT EXISTS filewatch (
                                filename TEXT,
                                path TEXT,
                                event_type TEXT,
                                timestamp TEXT )
                                """)

    @patch('sqlite3.connect')
    def test_add_row(self, mock_connect):
        """Test if data is added to database."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        row = ("test.txt", "/path/to/file", "CREATE", "2025-03-20 10:00:00")
        db.add_row(row)
        query = "INSERT INTO filewatch (filename, path, event_type, timestamp) VALUES (?, ?, ?, ?)"
        mock_cursor.execute.assert_any_call(query, row)


    @patch('sqlite3.connect')
    def test_query_data(self, mock_connect):
        """Test if query is working, returns correct data."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        extension = "txt"
        event_type = "CREATE"
        date = "2025-03-20"
        t1 = "10:00:00"
        t2 = "12:00:00"
        db.query_data(extension, event_type, date, t1, t2)

        query = ("SELECT * FROM filewatch WHERE 1=1 AND filename LIKE ? AND event_type LIKE ? "
                 "AND STRFTIME('%F', timestamp) = ? AND STRFTIME('%T', timestamp) > ? "
                 "AND STRFTIME('%T', timestamp) < ?")
        args = ('%txt%', '%CREATE%', '2025-03-20', '10:00:00', '12:00:00')
        mock_cursor.execute.assert_called_with(query, args)


    @patch('sqlite3.connect')
    @patch('builtins.open', new_callable=MagicMock)
    def test_write_database(self, mock_open, mock_connect):
        """Test if database is written to the file."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        export_file = "/path/to/export"
        file_name = "export.sql"

        db.write_database(export_file, file_name)

        export_path = "/path/to/export/export.sql"

        mock_open.assert_called_once_with(export_path, 'w')


    @patch('sqlite3.connect')
    def test_delete_record(self, mock_connect):
        """Test if data is deleted from the database table."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        db.delete_record()

        mock_cursor.execute.assert_called_with("DELETE FROM filewatch")
        mock_conn.commit.assert_called()

    @patch('sqlite3.connect')
    def test_export_db_to_csv(self, mock_connect):
        """Test if database is exported as csv."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        filename = db.export_db_to_csv()

        mock_cursor.execute.assert_called_with("SELECT * FROM filewatch")
        self.assertEqual(filename, 'filewatch.csv')

    @patch('sqlite3.connect')
    def test_close(self, mock_connect):
        """Test if database is closed."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DatabaseManager()
        db.close()

        mock_conn.close.assert_called_once()
        mock_cursor.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
