# ytget

Easily get data and download YouTube videos, focused on speed and simplicity.

Also works as a command-line extractor/downloader.

## Installation

You can install `ytget` using pip:

```bash
pip install ytget
```
---
## Features

- Simple use.
- Quick download and info extraction of youtube videos and playlists.
- Quick youtube search.
- Access to age restricted videos without login.
- Access to your private videos logging into your account.
- Command-line support.
---
## Usage

### Python

To extract information from a video, create a `Video` object with the url or query:
```python
from ytget import Video

video = Video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Get info
title = video.title
duration = video.duration
subtitles = video.subtitles
stream_url = video.stream_url
# ...and so on. 
# You can use print(dir(video)) or help(video) to get all available info and parameters.

# Download the video
video.download()

# Change some parameters
video.download(path="downloads/", quality="med", only_audio=True)
```

You can also search for a query and get the information of all the videos obtained:
```python
from ytget import Search
from ytget.utils import format_seconds

# Get the complete information of all videos
results = Search("never gonna give you up", get_duration_formatted=False).results

# Download all
results.download()

for result in results:
    # Only download if the video is less than 3 minutes long
    if result.duration < format_seconds('3:00'):
        result.download(quality="best", only_video=True, target_fps=30)


# Get simplified information (in case you need speed and don't need to download)
results = Search("never gonna give you up", get_simple=True).results

for result in results:
    print(result['title'], result['url'])
```

Get information from a playlist:
```python
from ytget import Playlist, Fetch

# Get the complete information of all videos
playlist = Playlist("https://www.youtube.com/watch?v=9OFpfTd0EIs&list=PLd9auH4JIHvupoMgW5YfOjqtj6Lih0MKw")

# Download all
playlist.download()

for video in playlist:
    print(video.get('title'), video.get('url'))

    
# Instead of downloading directly, you can do something with the videos before
videos = playlist.videos

for video in videos:
    # Download videos starting with the letter a
    if video.title.lower().startswith('a'):
        video.download()

        
# If you want to be the most efficient, get only the initial data of each video
videos_info = list(filter(lambda x: x.get('title').lower().startswith('b'), playlist.videos_info))

videos_to_download = Fetch(videos_info)
for video in videos_to_download:
    video.download()
```

### Command-line
For more detailed information, use:
```bash
ytget --help
```

Example 1 - Downloading a video and printing its title and url:
```bash
ytget https://www.youtube.com/watch?v=dQw4w9WgXcQ --print title url
```

Example 2 - Searching for a query, without downloading get the data of all the videos and write it to a json file:
```bash
ytget "never gonna give you up" --search --skip-download --print all --write-to-json
```

Example 3 - Get playlist info (with a maximum of 150 videos) and write to json file their titles, urls and ids:
```bash
ytget "https://www.youtube.com/playlist?list=PLd9auH4JIHvupoMgW5YfOjqtj6Lih0MKw" --max-length 150 --print title url video_id --skip-download --write-to-json
```
---
### To Do
- ~~Add playlist support.~~
- Add channels support.
- Allow some way to download livestreams (fractions).
- Make user input download speed in MB/s and not using chunk size.

### Known issues
- Issues related to downloading age restricted videos with and without logging in.
- When downloading some specific formats the result might be "corrupted". For now this can be fixed by enabling "force_ffmpeg".

### Repository

The source code is available on [GitHub](https://github.com/Coskon/ytget).

### License

This project is licensed under the MIT License.