#!usr/bin/python


from pytube import YouTube


def get_information(url: str):
    yt = YouTube(url)
    return yt


def get_download_information(yt: YouTube, instruction, path):
    if instruction == "video_and_audio":
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        return tuple((stream, path, stream.default_filename + "_video_and_audio" + stream.resolution))

    elif instruction == "audio":
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        return tuple((stream, path, stream.default_filename + "_nur_audio"))

    elif instruction == "audio-convert":
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        return tuple((stream, path + "/tmp", stream.default_filename))

    elif instruction == "video":
        stream = yt.streams.filter(only_video=True, file_extension="mp4").order_by("resolution").desc().first()
        return tuple((stream, path, stream.default_filename + "_nur_video" + stream.resolution))

    elif instruction == "choose":
        while True:
            print("Folgende Downloads sind verfügbar:")
            print("Nur Video:")
            streams = []
            name_extensions = []
            count = 0
            for stream in yt.streams.filter(only_video=True, file_extension="mp4").order_by("resolution").desc():
                print("[" + str(count) + "]: ", end="")
                if count < 10:
                    print(" ", end="")
                print(stream.resolution, "      stream_data:", stream)
                streams.append(stream)
                name_extensions.append("_nur_video")
                count += 1

            print("Video und Audio:")
            for stream in yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc():
                print("[" + str(count) + "]: ", end="")
                if count < 10:
                    print(" ", end="")
                print(stream.resolution, "      stream_data:", stream)
                streams.append(stream)
                name_extensions.append("_video_and_audio")

                count += 1

            print("Nur Audio: ")
            streams.append(yt.streams.filter(only_audio=True, file_extension="mp4").first())
            name_extensions.append("_nur_audio")
            print("[" + str(count) + "]: ", end="")
            if count < 10:
                print(" ", end="")
            print("mp4 Format beibehalten")
            count += 1

            streams.append(yt.streams.filter(only_audio=True, file_extension="mp4").first())
            name_extensions.append("")
            print("[" + str(count) + "]: ", end="")
            if count < 10:
                print(" ", end="")
            print("zu mp3 konvertieren")
            d = input("Welche Downloads möchtest du? Mehrere Eingaben sind durch ein Komma zu trennen!").split(",")
            to_download = {}
            for di in d:
                try:
                    n = int(di.strip())
                    stream = streams[n]
                    to_download[n] = stream
                except:
                    print("Erlaubte Eingaben sind Zahlen zwischen 0 und", count)
                    continue

            to_return = []

            for i, stream in to_download.items():
                if name_extensions[i] == "":
                    to_return.append(tuple((stream, path + "/tmp", stream.default_filename[:20])))
                elif stream.is_progressive or stream.includes_video_track:
                    to_return.append(
                        tuple((stream, path, stream.default_filename[:20] + name_extensions[i] + stream.resolution)))
                else:
                    to_return.append(tuple((stream, path, stream.default_filename[:20] + name_extensions[i])))

            return to_return


def download(stream, path, name):
    stream.download(output_path=path, filename=name)
