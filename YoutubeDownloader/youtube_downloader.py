#!/usr/bin/python3
import os
from threading import Thread
from pytube import YouTube
from pytube.streams import Stream
from pytube.exceptions import VideoUnavailable
from moviepy.editor import AudioFileClip


def read() -> list[str]:
    videos = []
    with open("./videos.txt", "r") as file:
        for line in file:
            if line.strip() != "":
                videos.append(line.strip())
    return videos


def get_yt(url: str) -> YouTube:
    return YouTube(url)


def get_yts(urls: list) -> list[YouTube]:
    yts = []
    for url in urls:
        yts.append(get_yt(url))
    return yts


def get_stream_full(yt: YouTube) -> Stream:
    stream = yt.streams.filter(progressive=True, file_extension="mp4") \
        .order_by("resolution").desc().first()
    return stream


def get_stream_video(yt: YouTube) -> Stream:
    stream = yt.streams.filter(only_video=True, file_extension="mp4") \
        .order_by("resolution").desc().first()
    return stream


def get_stream_audio(yt: YouTube) -> Stream:
    stream = yt.streams.filter(only_audio=True, file_extension="mp4") \
            .order_by("abr").desc().first()
    return stream


def get_stream_choose(yt: YouTube) -> list[Stream]:
    streams = []
    print("Folgende Downloads sind verfügbar:")

    print("Video und Audio:")
    available_streams = yt.streams
    for stream in available_streams \
            .filter(progressive=True, file_extension="mp4") \
            .order_by("resolution").desc():
        print(f"[{str(len(streams)).zfill(2)}]: {stream.resolution}\t\tgenaue Daten: {stream}")
        streams.append(stream)

    print("Nur Video:")
    for stream in available_streams \
            .filter(only_video=True, file_extension="mp4") \
            .order_by("resolution").desc():
        print(f"[{str(len(streams)).zfill(2)}]: {stream.resolution}\t\tgenaue Daten: {stream}")
        streams.append(stream)

    print("Nur Audio:")
    for stream in available_streams \
            .filter(only_audio=True, file_extension="mp4") \
            .order_by("abr").desc():
        print(f"[{str(len(streams)).zfill(2)}]: {stream.abr}\t\tgenaue Daten: {stream}")
        streams.append(stream)

    print("Was soll gedownloadet werden?")
    print("Mehrere Eingaben sind durch ein Komma zu trennen")
    wanted = input("Eingabe: ")
    to_download = []
    for index in wanted.split(","):
        try:
            index = int(index)
        except ValueError:
            print(f"Erlaubte Eingaben sind Zahlen zwischen 0 und {len(streams)-1}")
            print(f"Eingabe {index} wird übersprungen")
            continue
        to_download.append(streams[index])

    return to_download


def main():
    def thread_worker():
        while len(streams) > 0:
            stream = streams.pop()
            working.append(stream)
            if stream.is_progressive:
                path = "./downloads/video_und_audio/"
            elif stream.includes_video_track and not stream.includes_audio_track:
                path = "./downloads/nur_video/"
            elif stream.includes_audio_track and not stream.includes_video_track:
                path = "./downloads/nur_audio/mp4/"
            print(f"Starte Download #{len(finished)+len(working)}"
            stream.download(output_path=path)
            working.remove(stream)
            finished.append(stream)

    videos = read()
    print(f"{len(videos)} Link(s) gefunden. Fortfahren (j/n) ", end="")
    if input().lower() != "j":
        print("Wird abgebrochen")
        return
    yts = get_yts(videos)
    print("Folgende Möglichkeiten:\n"
          "1: Bei allen Videos die höchste Auflösung herunterladen\n"
          "2: Bei allen Videos die höchste Auflösung, aber ohne Ton herunterladen\n"
          "3: Bei allen Videos nur das Audio herunterladen\n"
          "4: Bei jedem Video einzeln entscheiden (mehr Optionen)")
    task = input("Eingabe: ")
    streams = []
    if task == "1":
        for yt in yts:
            try:
                streams.append(get_stream_full(yt))
            except VideoUnavailable:
                print(f"Video {yt.watch_url} konnte nicht gefunden werden")
    elif task == "2":
        for yt in yts:
            try:
                streams.append(get_stream_video(yt))
            except VideoUnavailable:
                print(f"Video {yt.watch_url} konnte nicht gefunden werden")
    elif task == "3":
        for yt in yts:
            try:
                streams.append(get_stream_audio(yt))
            except VideoUnavailable:
                print(f"Video {yt.watch_url} konnte nicht gefunden werden")
    elif task == "4":
        for yt in yts:
            try:
                streams.extend(get_stream_choose(yt))
            except VideoUnavailable:
                print(f"Video {yt.watch_url} konnte nicht gefunden werden")
    else:
        print("Ungültige Eingabe")
        return

    print(f"{len(streams)} Download(s) sind/ist bereit gestartet zu werden")
    print("Wie viele Downloads sollen parallel laufen?")
    print("Empfehlung: Je besser die Internetgeschwindigkeit, desto mehr")
    while True:
        parallel_downloads = input("Eingabe: ")
        try:
            parallel_downloads = int(parallel_downloads)
            break
        except ValueError:
            print("Nur Zahlen sind als Eingabe erlaubt")
    working = []
    finished = []
    threads = []
    for _ in range(parallel_downloads):
        t = Thread(target=thread_worker)
        threads.append(t)
        t.start()
    print("Alle Prozesse laufen")
    for thread in threads:
        thread.join()
    print("Alle Downloads fertig")

    if not os.listdir("./downloads/nur_audio/mp4/"):
        return
    print("Es gibt Audio Dateien die noch nicht zu mp3 Dateien konvertiert wurden")
    print("Sollen diese konvertiert werden? (j/n) ", end="")
    if input().lower() != "j":
        print("Dateien werden nicht konvertiert")
        return
    for file in os.listdir("./downloads/nur_audio/mp4/"):
        clip = AudioFileClip("./downloads/nur_audio/mp4/"+file)
        clip.write_audiofile("./downloads/nur_audio/mp3/"+file[:-4]+".mp3")
        clip.close()
        os.remove("./downloads/nur_audio/mp4/"+file)
    print("Alle Dateien konvertiert!")


if __name__=="__main__":
    main()
    print("Fertig!")
    input("Drücke Enter zum Schließen")
