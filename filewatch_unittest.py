import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from filewatch import FileWatch, FileHandler
from databasemanager import DatabaseManager


class TestFileHandler(unittest.TestCase):

    @patch('databasemanager.DatabaseManager')
    @patch('filewatch.Controller')
    def test_log_event(self, MockController, MockDatabaseManager):
        """Test if function call controller add row with correct information."""
        # Arrange
        mock_controller = MockController()
        mock_database = MockDatabaseManager()
        file_handler = FileHandler(mock_controller, mock_database, extension=[".txt", ".csv"])

        mock_controller.add_row = MagicMock()
        mock_event = MagicMock()
        mock_event.src_path = '/some/path/to/file/test_file.txt'
        mock_event.is_directory = False

        filename = "test_file.txt"
        filepath = "/some/path/to/file"
        event_type = "Created"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = (filename, filepath, event_type, timestamp)


        file_handler.on_created(mock_event)
        mock_controller.add_row.assert_called_with(row)


class TestFileWatch(unittest.TestCase):

    @patch('filewatch.FileHandler')
    @patch('filewatch.Observer')
    @patch('filewatch.Controller')
    def test_start_monitoring(self, MockController, MockObserver, MockFileHandler):
        """Test if monitoring is started."""
        mock_model = MagicMock()
        mock_view = MagicMock()
        mock_controller = MockController()

        mock_observer = MagicMock()
        MockObserver.return_value = mock_observer
        mock_file_handler = MockFileHandler(mock_controller, mock_model, [])
        mock_controller.add_row = MagicMock()
        mock_view.check.return_value = 1

        file_watch = FileWatch(mock_model, mock_view)
        file_watch.monitoredFile = ["/path/to/monitor"]
        file_watch.extension = ".txt"

        file_watch.start()
        MockObserver.assert_called_once()
        mock_observer.schedule.assert_called_once_with(mock_file_handler, ["/path/to/monitor"], recursive=True)
        mock_observer.start.assert_called_once()

    @patch('filewatch.FileHandler')
    @patch('filewatch.Observer')
    @patch('filewatch.Controller')
    def test_stop_monitoring(self, MockController, MockObserver, MockFileHandler):
        """Test if monitoring is stopped."""
        mock_model = MagicMock()
        mock_view = MagicMock()
        mock_controller = MockController()

        mock_observer = MagicMock()
        MockObserver.return_value = mock_observer

        file_watch = FileWatch(mock_model, mock_view)
        file_watch.monitoredFile = ["/path/to/monitor"]
        file_watch.extension = ".txt"

        mock_observer.is_alive.return_value = True

        file_watch.start()
        file_watch.stop()
        mock_observer.stop.assert_called_once()
        mock_observer.join.assert_called_once()


if __name__ == '__main__':
    unittest.main()