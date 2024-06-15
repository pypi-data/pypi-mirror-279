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
- Quick download and info extraction of youtube videos.
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
---
### To Do
- Add playlist support.
- Add channels support.
- Allow some way to download livestreams (fractions).
- Make user input download speed in MB/s and not using chunk size.

### Repository

The source code is available on [GitHub](https://github.com/Coskon/ytget).

### License

This project is licensed under the MIT License.