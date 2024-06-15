import pathlib
import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime

CACHE_DIR = pathlib.Path(__file__).parent.resolve() / '__cache__'
ACCESS_TOKEN_DIR = os.path.join(CACHE_DIR, 'access_token.json')
CLIENT_ID = '861556708454-d6dlm3lh05idd8npek18k6be8ba3oc68.apps.googleusercontent.com'
CLIENT_SECRET = 'SboVhoG9s0rNafixCSGGKXAT'
CLIENT_INFO = {
    "android_music": {
        "payload": {
            "context": {
                "client": {
                    "clientName": "ANDROID_MUSIC",
                    "clientVersion": "5.16.51",
                    "androidSdkVersion": 30
                }
            },
            "racyCheckOk": True,
            "contentCheckOk": True
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
            "Origin": "https://music.youtube.com",
            "X-Youtube-Client-Name": "67",
            "X-Youtube-Client-Version": "1.20240610.01.00",
            "X-Youtube-Device": "cbr=Chrome+Mobile&cbrand=google&cbrver=125.0.0.0&ceng=WebKit&cengver=537.36&cmodel=nexus+5&cos=Android&cosver=6.0&cplatform=MOBILE",
        }
    },
    "tv_embed": {
        "payload": {
            "context": {
                "client": {
                    "clientName": "TVHTML5_SIMPLY_EMBEDDED_PLAYER",
                    "clientVersion": "2.0",
                },
            },
            'racyCheckOk': True,
            'contentCheckOk': True
        },
        "headers": {
            "X-YouTube-Client-Name": "85",
            "X-YouTube-Client-Version": "2.0",
            "Origin": "https://www.youtube.com"
        }
    },
    "android": {
        "payload": {
            "context": {
                "client": {
                    "clientName": "ANDROID",
                    "clientVersion": "17.31.35",
                    "client": "MWEB",
                    "androidSdkVersion": 30
                }
            },
            "racyCheckOk": True,
            "contentCheckOk": True
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Origin": "https://m.youtube.com",
            "X-Youtube-Client-Name": "2",
            "X-Youtube-Client-Version": "2.20240612.01.00",
            "X-Youtube-Device": "cbr=Chrome+Mobile&cbrand=samsung&cbrver=116.0.0.0&ceng=WebKit&cengver=537.36&cmodel=sm-g981b&cos=Android&cosver=13&cplatform=MOBILE",
        }
    },
    "android_creator": {
        "payload": {
            "context": {
                "client": {
                        "clientName": "ANDROID_CREATOR",
                        "clientVersion": "2.20240613.01.00"
                    }
                },
            "racyCheckOk": True,
            "contentCheckOk": True
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Origin": "https://studio.youtube.com",
            "X-Youtube-Client-Name": "62",
            "X-Youtube-Client-Version": "1.20240612.00.00",
            "X-Youtube-Device": "cbr=Chrome+Mobile&cbrand=google&cbrver=125.0.0.0&ceng=WebKit&cengver=537.36&cmodel=nexus+5&cos=Android&cosver=6.0&cplatform=MOBILE",
        }
    },
    "web": {
        "payload": {
            "context": {
                "client": {
                        "clientName": "WEB",
                        "clientVersion": "2.20240613.01.00",
                    }
                },
            "racyCheckOk": True,
            "contentCheckOk": True,
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Origin": "https://www.youtube.com",
            "X-Youtube-Client-Name": "1",
            "X-Youtube-Client-Version": "2.20240613.01.00",
            "X-Youtube-Device": "cbr=Chrome&cbrver=125.0.0.0&ceng=WebKit&cengver=537.36&cos=Windows&cosver=10.0&cplatform=DESKTOP",
            "Cache-Control": "max-age=0"
        }
    },
}
AVAILABLE_CLIENTS = list(CLIENT_INFO.keys())

YOUTUBE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept-Language': 'en-us,en;q=0.5',
    'Sec-Fetch-Mode': 'navigate',
    'X-Youtube-Client-Name': '1',
    'X-Youtube-Client-Version': '17.19.36',
    'X-Goog-Visitor-Id': 'Cgs2RldTYzNiVVZoUSj9062zBjIKCgJBUhIEGgAgUA%3D%3D',
}

LOWEST_KEYWORDS = {'worst', 'lowest', 'least', 'bad'}
LOW_KEYWORDS = {'low', 'poor'}
MEDIUM_KEYWORDS = {'med', 'mid', 'medium', 'normal'}
HIGH_KEYWORDS = {'high', 'good'}


def _format_date(date, format_type):
    formatted = date
    dt = datetime.fromisoformat(date)
    if format_type == 'eu':  # DD/MM/YYYY HH:MM:SS
        formatted = f"{dt.day:02}/{dt.month:02}/{dt.year:04} {dt.hour:02}:{dt.minute:02}:{dt.second:02}"
    elif format_type == 'us':  # MM/DD/YYYY HH:MM:SS AM/PM
        formatted = f"{dt.month:02}/{dt.day:02}/{dt.year:04} {dt.strftime('%I'):02}:{dt.minute:02}:{dt.second:02} {dt.strftime('%p')}"
    elif format_type == 'sql':  # YYYY-MM-DD HH:MM:SS
        formatted = f"{dt.year:04}-{dt.month:02}-{dt.day:02} {dt.hour:02}:{dt.minute:02}:{dt.second:02}"
    elif format_type == 'unix':
        formatted = dt.timestamp()

    return formatted


def _format_title(title: str):
    return re.sub(r'[<>:"/\\|?*]', '_', str(title))


def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours == 0:
        return "{:0}:{:02d}".format(int(minutes), int(seconds))
    else:
        return "{:0}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))


def _format_views(views, replace_character=" "):
    if views.isnumeric(): return views
    views = views[::-1]
    return replace_character.join([views[i:i + 3] for i in range(0, len(views), 3)])[::-1]


def formatted_to_seconds(time_str):
    if not time_str: return
    time_components = time_str.split(':')
    num_components = len(time_components)
    hours = 0
    if num_components == 3:
        hours = int(time_components[0])
        minutes = int(time_components[1])
        seconds = int(time_components[2])
    else:
        minutes = int(time_components[0])
        seconds = int(time_components[1])
    return hours * 3600 + minutes * 60 + seconds


def _get_chapters(desc):
    desc = desc+"\n"
    chapters = re.findall(r"((\(?\d{1,3}:\d{2}(?::\d{2})?\)?)\s+(.*?)\n)|((.*?)\s+(\(?\d{1,3}:\d{2}(?::\d{2})?\)?)\n)", desc)
    if not chapters: return
    return [{'timestamp': re.sub(r'[()]', '', chapter[1].strip()) if chapter[1] != ""
            else re.sub(r'[()]', '', chapter[-1].strip()),
             'name': chapter[2].strip() if chapter[2] != ""
            else re.sub(r'[()]', '', chapter[4].strip())} for chapter in chapters]


def _get_channel_picture(channel_url):
    response = requests.get(channel_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        meta_tag = soup.find('meta', {'property': 'og:image'})
        if meta_tag:
            image_url = meta_tag.get('content')
            return image_url
    return None


def _is_url(query):
    return bool(re.compile(r"^(https?://)?(www\.)?[\w.-]+\.\w+/?.*$").match(query))


def _is_valid_yt_url(query):
    yt_pattern = r"(?:v=|\/videos\/|embed\/|\.be\/|\/v\/|\/e\/|watch\/|shorts\/|live\/|\/oembed\?url=https:\/\/www\.youtube\.com\/watch\?v=|watch%3Fv%3D|shorts\/|attribution_link\?a=.*&u=\/watch%3Fv%3D|attribution_link\?a=.*&u=https:\/\/www\.youtube\.com\/watch\?v%3D|attribution_link\?a=.*&u=https:\/\/www\.youtube\.com\/embed\/|attribution_link\?a=.*&u=\/embed\/|attribution_link\?a=.*&u=https:\/\/www\.youtube-nocookie\.com\/embed\/|attribution_link\?a=.*&u=\/e\/)([a-zA-Z0-9_-]{11})"
    yt_match = re.search(yt_pattern, query)
    if yt_match:
        return True, yt_match.group(1)
    elif _is_url(query):
        http_str = 'http://' if 'https://' not in query and 'http://' not in query else ''
        yt_match = re.search(yt_pattern, requests.head(http_str + query, allow_redirects=True).url)
        if yt_match:
            return True, yt_match.group(1)
        return False, False
    return False, None


def _convert_captions(captions_url):
    soup = BeautifulSoup(requests.get(captions_url).text, 'html.parser')
    transcript = soup.find_all('text')

    data = []
    for text in transcript:
        timestamp = text.get('start')
        duration = text.get('dur')
        content = text.text
        data.append({
            'timestamp': float(timestamp),
            'ftimestamp': format_seconds(float(timestamp)),
            'duration': float(duration),
            'fduration': format_seconds(float(duration)),
            'text': content
        })
    return data
