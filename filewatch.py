from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime
from mvc import Controller

class FileHandler(FileSystemEventHandler):
    def __init__(self, controller,  database, extension=None):

        self.__extension = extension
        self.__filename = None
        self.__filepath = None
        self.__controller = controller
        self.__database = database

    def on_modified(self, event):
        """Watch for modified files."""
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)  # Extract just the filename
        ext = os.path.splitext(self.__filename)[1]
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Modified')
        elif not self.__extension:
            self.log_event('Modified')

    def on_created(self, event):
        """Watch for created files."""
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)  # Extract just the filename
        ext = os.path.splitext(self.__filename)[1]
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Created')
        elif not self.__extension:
            self.log_event('Created')

    def on_deleted(self, event):
        """Watch for deleted files."""
        if event.is_directory: return None
        self.__filename = os.path.basename(event.src_path)  # Extract just the filename
        ext = os.path.splitext(self.__filename)[1]
        self.__filepath = os.path.dirname(event.src_path)
        if ext.lower() in self.__extension:
            self.log_event('Deleted')
        elif not self.__extension:
            self.log_event('Deleted')

    def log_event(self, event_type):
        """Log an event and call controller to add event to database."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = self.__filename, self.__filepath, event_type, timestamp
        self.__controller.add_row(row)


        #on_any_event: Executed for any event.
        #on_created: Executed upon creation of a new file or directory.
        #on_modified: Executed upon modification of a file or when a directory is renamed.
        #on_deleted: Triggered upon the deletion of a file or directory.
        #on_moved: Triggered when a file or directory is relocated.
class FileWatch(Controller):
    def __init__(self, model, view):
        super().__init__(model, view)
        self.__observer = None
        self.__extension = []
        self.__monitoredFile = []
        self.__model = model
        self.__view = view
        self.__handler = FileHandler(self, model, self.__extension)
        

    @property
    def monitoredFile(self):
        """Property getter for monitored file."""
        return self.__monitoredFile

    @monitoredFile.setter
    def monitoredFile(self, value):
        """Property setter for monitored file."""
        self.__monitoredFile = value

    @property
    def extension(self):
        """Property getter for extension."""
        return self.__extension
    @extension.setter
    def extension(self, extension):
        """Property setter for extension."""
        self.__extension.append(extension)


    def start(self):
        """Start monitoring the file."""
        if not self.__monitoredFile:
            print('No file to watch')
            return

        if not self.__observer or not self.__observer.is_alive():
            self.__observer = Observer()
        # Create a new observer instance
        get_check = self.__view.check()
        if get_check == 1:
            self.__observer.schedule(self.__handler, self.monitoredFile, recursive=True)
            self.__observer.start()
        else:
            self.__observer.schedule(self.__handler, self.monitoredFile, recursive=False)
            self.__observer.start()
        print("Monitoring started.")

        print('Starting file watch... Press Stop to stop')



    def stop(self):
        """Stop monitoring the file."""
        print('Stopping file watch...')
        if self.__observer.is_alive():
            self.__observer.stop()
            self.__observer.join()  # Wait for the observer to finish its work

            print("Monitoring stopped.")
        else:
            print("Monitoring is not running.")




