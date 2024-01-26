from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# import insert_image_data_test as insert_image

# Todo: Parsern måste fungera för att automatiskt läggas in i db, fixa rätt path i servern
#Event Handler that checks if a file is added. Then it shall parse the filename and add it to the db.
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("File added", event.src_path)
            # insert_image.add_data(event.src_path, "andra parametern till parsern?") Här skall den läggas in automatiskt in i databasen med hjälp av parsern.

    def on_deleted(self, event):
        print("File deleted")  # Behövs det upptäckas ifall filer tas bort? Isåfall skall de tas bort från db?


# Function to observe the FTP path
def Listener():
    path = "./test/" # fixa rätt path i server-miljö
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print("Listener:", path)
    observer.join()


Listener()
