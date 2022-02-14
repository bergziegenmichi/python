from pytube import YouTube
yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
for stream in yt.streams.filter(only_audio=True):
    print(stream)
