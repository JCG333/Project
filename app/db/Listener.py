from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print("Directory created")
        else:
            print("File added")


def Listener(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print("Listener:", path)
    observer.join()

if __name__ == "__main__":
    folder_path = "" # Byt ut detta mot rätt path.
    Listener(folder_path)
