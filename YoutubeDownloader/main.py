#!/usr/bin/python3

import downloader
from threading import Thread
import os.path
import shutil
from moviepy.editor import AudioFileClip


def thread_worker(url, results):
    results.append(downloader.get_information(url))



videos = []

with open("./videos.txt", "r") as f:
    for line in f:
        if line.strip() != "":
            videos.append(line.strip())



threads = []
results = []

for video in videos:
    t = Thread(target=thread_worker, args=(video, results))
    threads.append(t)
    t.start()

while True:
    what_to_do = input("Es gibt folgende Möglichkeiten:\n"
                       "1: Bei allen Videos das Video und das Audio (in einer Datei) "
                       "mit der höchsten Auflösung herunterladen.\n"
                       "2: Bei allen Videos nur das Audio herunterladen.\n"
                       "3: Bei allen Videos nur das Video mit der höchsten Auflösung herunterladen.\n"
                       "4: Bei jedem Video einzeln entscheiden.\n"
                       "Schreibe 1, 2, 3 oder 4! ")
    if what_to_do == "1":
        instruction = "video_and_audio"
        break

    elif what_to_do == "2":
        while True:
            convert = input("Es werden mp4 Dateien heruntergeladen. Sollen diese zu mp3 konvertiert werden? (j/n): ")
            if convert.lower() == "j":
                instruction = "audio-convert"
                break
            elif convert.lower() == "n":
                instruction = "audio"
                break
            else:
                print("Unerlaubte Eingabe!\n\n")
        break

    elif what_to_do == "3":
        instruction = "video"
        break

    elif what_to_do == "4":
        instruction = "choose"
        break

    else:
        print("Unerlaubte Eingabe!\n\n")

print("\n\n")

while True:
    path = input("Gib den Pfad ein wo die Dateien gespeichert werden sollen.\n"
                 "Beispiel: C:/Users/michael/Documents/YoutubeDownloads\n"
                 "Info: Backslashes (\"\\\") können durch normale Slashes (\"/\") ersetzt werden.\n"
                 "Info: Es werden temporäre Ordner an dieser Stelle erstellt, die danach automatisch gelöscht werden.\n"
                 "    Diese nicht löschen, außer nach einem Absturz des Programms! Auch das ist aber nicht notwendig.\n"
                 'Achtung: Der Ordner muss leer sein!.\n'
                 "Achtung: Es sind Schreibberechtigungen erforderlich!\n")

    if not os.path.exists(path):
        print("Dieser Pfad existiert nicht!\n\n")

    elif os.path.isfile(path):
        print("Dieser Pfad ist eine Datei und kein Ordner!\n\n")

    elif len(os.listdir(path)) != 0:
        print("Dieser Ordner ist nicht leer!\n\n")

    else:
        try:
            os.makedirs(path + "/test")
            os.mknod(path+"/test/test.txt")
            shutil.rmtree(path + "/test")
            break
        except Exception as e:
            if input("Keine Schreibberechtigungen vorhanden!\n"
                     "Drücke Enter!\n\n") != "":
                print(e)

try:
    shutil.rmtree(path + "/tmp")
except FileNotFoundError:
    pass
finally:
    os.makedirs(path + "/tmp")


print("Informationen über die Videos werden gesucht. Eventuell sind noch weitere Eingaben notwendig!")


downloads = []


for result in results:
    r = downloader.get_download_information(result, instruction, path)
    if type(r) == list:
        for element in r:
            downloads.append(element)
    else:
        downloads.append(r)

print("Ab jetzt sind keine weiteren Benutzereingaben mehr notwendig.")
print("Eventuell wurden noch nicht alle Informationen über die Videos gesammelt.")
print("Bitte warten...")

for thread in threads:
    thread.join()

print("Alle Informationen gesammelt. Die Downloads können jetzt beginnen")
input("Drücke Enter zum Starten!")

threads = []

for download in downloads:
    t = Thread(target=downloader.download, args=download)
    threads.append(t)
    t.start()

print("Alle Downloads gestartet!")

for thread in threads:
    thread.join()

print("Alle Downloads fertig!")


print("Jetzt werden die mp4 Dateien zu mp3 konvertiert!")

for file_name in os.listdir(path+"/tmp"):
    clip = AudioFileClip(path+"/tmp/"+file_name)
    clip.write_audiofile(path+"/"+file_name[:-4]+"_nur_audio.mp3")
    clip.close()

print("Alle Dateien konvertiert!")


shutil.rmtree(path+"/tmp")
input("Drücke Enter zum Schließen!")
