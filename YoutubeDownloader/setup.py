import os

os.mkdir("./downloads/")
os.mkdir("./downloads/video_und_audio/")
os.mkdir("./downloads/nur_video/")
os.mkdir("./downloads/nur_audio/")
os.mkdir("./downloads/nur_audio/mp3")
os.mkdir("./downloads/nur_audio/mp4")
open("./videos.txt", "a").close()

os.system("pip install git+https://github.com/JavDomGom/pytube")
os.system("pip install moviepy")
