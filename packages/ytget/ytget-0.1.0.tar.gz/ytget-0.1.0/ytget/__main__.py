import os
import json
import re
import subprocess
import warnings

import requests

from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from colorama import just_fix_windows_console
from tqdm import tqdm

from .exceptions import (SearchError, ExtractError, DownloadError, ForbiddenError)
from .utils import (CACHE_DIR, ACCESS_TOKEN_DIR, CLIENT_ID, CLIENT_SECRET, CLIENT_INFO, AVAILABLE_CLIENTS,
                    YOUTUBE_HEADERS, LOWEST_KEYWORDS, LOW_KEYWORDS, MEDIUM_KEYWORDS, HIGH_KEYWORDS,
                    _format_date, _format_views, format_seconds, formatted_to_seconds, _format_title,
                    _get_chapters, _get_channel_picture, _is_valid_yt_url, _convert_captions)
from .out_colors import (_red, _dim_cyan, _dim_yellow, _green)


warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
just_fix_windows_console()


class Video:
    """
    Get data from a YouTube video.

    Attributes
    ----------
    query: str
        A YouTube URL or query to search for.
        To get multiple video data for a query, use the `Search` class instead.
    kwargs: dict (Default parameters)
        get_duration_formatted: bool (True) - Retrieve the duration of the video formatted as HH:MM:SS instead of seconds.
        get_channel_picture: bool (True) - Retrieve the channel picture (slow down by ~0.3s)
        get_thumbnail: bool (True) - Retrieve the thumbnail.
        thumbnail_quality: str ("best") - Quality of the thumbnail to retrieve ("best", "high", "med", "low")
        get_subtitles: bool (True) - Retrieve the subtitles of the video.
        get_chapters: bool (True) - Retrieve the chapters of the video.
        get_stream: bool (True) - Retrieve the stream url.
        get_date: bool (True) - Retrieve publish and upload date.
        get_date_formatted: bool (True) - Format the date to be more readable.
        date_format: str ("eu") - Way to format the date ("eu", "us", "sql", "unix")
        use_login: bool (False) - Login into an account.
        disable_cache: bool (False) - Disable auth cache. Needs login everytime instead.
        ignore_errors: bool (False) - In case of error (not fatal), proceed anyways.
        ignore_warnings: bool (False) - Don't print warnings on screen.
        verbose: bool (True) - Show information/warnings on screen.
        no_retry: bool (False) - Allow retries in case extraction/download fails with the set client.
        client: str ("android_music") - Client to use. ("android", "tv_embed", "android_music", "android_creator", "web")

    Methods
    -------
    download(path=".", quality="best", only_audio=False, only_video=False, target_fps=-1, target_itag=-1,
            preferred_video_format="mp4", preferred_audio_format = "mp3", chunk_size=1024*1024, force_ffmpeg=False)
        Downloads an appropriate video/audio stream.

        path: str - Output path.
        quality: str - Quality of the stream (by bitrate): "best", "high", "med", "low", "lowest".
        only_audio: bool - Gets a stream with only audio data.
        only_video: bool - Gets a stream with only video data.
        target_fps: int - Target fps of the video, preferred over bitrate.
        target_itag: int - Target itag of the stream to download.
        preferred_video_format: str - Video format to download into.
        preferred_audio_format: str - Audio format to download into (for only_audio=True).
        chunk_size: int - Stream download chunk size.
        force_ffmpeg: bool - Force the conversion to bytes to be made using ffmpeg, use it for format conversion.
    """
    def __init__(self, query, **kwargs):
        """Make a Video class.

        :param str query:
            A YouTube URL or query to search for.
        :param dict kwargs:
            Extra arguments to parse. Use help(Video) for more info.
        """
        parameters = {
            "get_duration_formatted": True,
            "get_channel_picture": True,
            "get_thumbnail": True,
            "thumbnail_quality": "best",
            "get_views_formatted": False,
            "get_subtitles": True,
            "get_chapters": True,
            "get_stream": True,
            "get_date": True,
            "get_date_formatted": True,
            "date_format": "eu",
            "use_login": False,
            "disable_cache": False,
            "ignore_errors": False,
            "ignore_warnings": False,
            "verbose": False,
            "no_retry": False,
            "client": AVAILABLE_CLIENTS[0]
        }
        invalid_params = []
        for param in kwargs:
            if param not in parameters:
                invalid_params.append(param)
        parameters.update(kwargs)
        self._ignore_errors = parameters.get("ignore_errors")
        self._ignore_warnings = parameters.get("ignore_warnings")
        self._verbose = parameters.get("verbose")
        self._no_retry = parameters.get("no_retry")
        self._client = parameters.get("client").lower()
        self._client_info = CLIENT_INFO[self._client].copy()
        if invalid_params:
            self._process_error(er_type="warning",
                                data={'message': f"The following parameters aren't valid: {', '.join(invalid_params)}",
                                      'is_fatal': False})

        self._use_login = parameters.get("use_login")
        self._disable_cache = parameters.get("disable_cache")
        access_token = None
        if parameters.get("use_login"):
            access_token = self._get_token()
        self._headers = self._get_headers(access_token=access_token)

        self._query = query.strip()
        is_valid_url = _is_valid_yt_url(self._query)

        self.video_id = self._search_query() if is_valid_url[1] is None else is_valid_url[1]
        if self.video_id is None:
            self._process_error(er_type="search", data={'query': query, 'is_fatal': True})
        elif not self.video_id:
            self.url = self._query
        else:
            self.url = "https://www.youtube.com/watch?v="+self.video_id
        self.json = self._extract_video_info()

        self._params = parameters
        self._get_data()

    def _get_data(self):
        parameters = self._params
        couldnt_extract = []
        self.video_info = self.json.get('videoDetails', {})
        if not self.video_info:
            self._process_error(er_type="extract",
                                data={'url': self.url, 'reason': '',
                                      'extract_type': 'video details (title, length, ...)',
                                      'message': f"Couldn't extract video details (title, length, ...) for {self.url}",
                                      'is_fatal': False})
        self.streaming_data = self.json.get('streamingData', {})
        if not self.streaming_data:
            self._process_error(er_type="extract",
                                data={'url': self.url, 'reason': '', 'extract_type': 'streaming data',
                                      'message': f"Couldn't extract streaming data for {self.url}", 'is_fatal': False})
        self.playability_status = self.json.get('playabilityStatus', {})
        if not self.playability_status:
            couldnt_extract.append('playability status')
        _captions = self.json.get('captions', {})
        if not _captions:
            couldnt_extract.append('captions data')
            self._captions_data = {}
        else:
            self._captions_data = _captions.get('playerCaptionsTracklistRenderer', {})
            if not self._captions_data:
                couldnt_extract.append('captions data')
        self._response_context = self.json.get('responseContext', {})
        if not self._response_context:
            couldnt_extract.append('response context')
        self._playback_tracking = self.json.get('playbackTracking', {})
        if not self._playback_tracking:
            couldnt_extract.append('playback tracking')
        self._tracking_params = self.json.get('trackingParams', {})
        if not self._tracking_params:
            couldnt_extract.append('tracking params')
        self._annotations = self.json.get('annotations', {})
        if not self._annotations:
            couldnt_extract.append('annotations')
        self._player_config = self.json.get('playerConfig', {})
        if not self._player_config:
            couldnt_extract.append('player config')
        self._storyboards = self.json.get('storyboards', {})
        if not self._storyboards:
            couldnt_extract.append('storyboards')
        self._microformat = self.json.get('microformat', {})
        if not self._microformat:
            couldnt_extract.append('microformat')
        self._cards = self.json.get('cards', {})
        if not self._cards:
            couldnt_extract.append('cards')
        self._attestation = self.json.get('attestation', {})
        if not self._attestation:
            couldnt_extract.append('attestation')
        self._messages = self.json.get('messages', {})
        if not self._messages:
            couldnt_extract.append('messages')
        self._endscreen = self.json.get('endscreen', {})
        if not self._endscreen:
            couldnt_extract.append('endscreen')
        self._ad_placements = self.json.get('adPlacements', {})
        if not self._ad_placements:
            couldnt_extract.append('ad placements')
        self._ad_breakheartbeat = self.json.get('adBreakHeartbeatParams', {})
        if not self._ad_breakheartbeat:
            couldnt_extract.append('ad break heartbeat params')
        self._framework_updates = self.json.get('frameworkUpdates', {})
        if not self._framework_updates:
            couldnt_extract.append('framework updates')
        self._process_error(er_type="warning",
                            data={'message': f"Couldn't extract {', '.join(couldnt_extract)} for {self.url}",
                                  'is_fatal': False})
        # vid info
        self.title = self.video_info.get('title')
        self._duration = int(self.video_info.get('lengthSeconds'))
        self.duration = format_seconds(self._duration) if parameters.get("get_duration_formatted") else self._duration
        self.keywords = self.video_info.get('keywords')
        self.channel_id = self.video_info.get('channelId')
        self.channel = self.video_info.get('author')
        self.channel_url = "https://www.youtube.com/channel/" + self.channel_id if self.channel_id else None
        self.channel_picture = _get_channel_picture(self.channel_url) if self.channel_url and parameters.get("get_channel_picture") else None
        self.description = self.video_info.get('shortDescription')
        self.chapters = _get_chapters(self.description) if self.description and parameters.get("get_chapters") else None
        if parameters.get("get_thumbnail"):
            tq = parameters.get("thumbnail_quality").lower()
            thumbnails = sorted(self.video_info['thumbnail']['thumbnails'], key=lambda x: x["width"], reverse=True)
            if tq in HIGH_KEYWORDS:
                thumbnail_data = thumbnails[1] if len(thumbnails) > 1 else thumbnails[0]
            elif tq in MEDIUM_KEYWORDS:
                thumbnail_data = thumbnails[2] if len(thumbnails) > 2 else thumbnails[0]
            elif tq in LOW_KEYWORDS | LOWEST_KEYWORDS:
                thumbnail_data = thumbnails[3] if len(thumbnails) > 3 else thumbnails[0]
            else:
                thumbnail_data = thumbnails[0]
            self.thumbnail = thumbnail_data.copy()
        else:
            self.thumbnail = None
        views = int(self.video_info.get('viewCount'))
        self.views = _format_views(str(views)) if parameters.get("get_views_formatted") else views
        self.is_live = bool(self.video_info.get('isLiveContent'))
        self.stream_url = self._get_stream().get('url') if parameters.get("get_stream") else None
        if parameters.get("get_date"):
            pd = self._microformat.get('playerMicroformatRenderer', {}).get('publishDate')
            ud = self._microformat.get('playerMicroformatRenderer', {}).get('uploadDate')
        else:
            pd, ud = None, None
        date_format = parameters.get("date_format").lower()
        self.publish_date = _format_date(pd, date_format) if pd and parameters.get('get_date_formatted') else pd
        self.upload_date = _format_date(ud, date_format) if ud and parameters.get('get_date_formatted') else ud

        # captions info
        self.subtitles = []
        if parameters.get("get_subtitles"):
            captions_data = self._captions_data.get('captionTracks')
            if captions_data:
                for caption in captions_data:
                    url, language, language_code = caption.get('baseUrl'), caption.get('name'), caption.get(
                        'languageCode')
                    self.subtitles.append({
                        'captions': _convert_captions(url),
                        'language': language.get('simpleText'),
                        'languageCode': language_code
                    })

    def download(self, path=".", quality="best", only_audio=False, only_video=False, target_fps=-1, target_itag=-1,
                 preferred_video_format="mp4", preferred_audio_format = "mp3", chunk_size=1024*1024, force_ffmpeg=False,
                 _raw_number=0):
        """
        Downloads an appropriate video/audio stream.

        Args:
        - path [str]: Output path. Defaults to the current directory.
        - quality [str]: Quality of the stream (by bitrate): "best", "high", "med", "low", "lowest". Defaults to "best".
        - only_audio [bool]: Gets a stream with only audio data. Defaults to False.
        - only_video [bool]: Gets a stream with only video data. Defaults to False.
        - target_fps [int]: Target fps of the video, preferred over bitrate. Defaults to -1 (ignore fps, order by bitrate).
        - target_itag [int]: Target itag of the stream to download. Defaults to -1 (no specific itag).
        - preferred_video_format [str]: Video format to download into. Defaults to "mp4".
        - preferred_audio_format [str]: Audio format to download into (for only_audio=True). Defaults to "mp3".
        - chunk_size [int]: Size of the chunks to download. Increase if you're experiencing low speeds, decrease if you want to limit. Defaults to 1024*1024.
        - force_ffmpeg [bool]: Force the conversion to bytes to be made using ffmpeg, use it for format conversion. Defaults to False.
        """

        def _download_chunk(url, start, end, pbar):
            response_content = requests.get(url, headers={'Range': f'bytes={start}-{end}'}, stream=True).content
            pbar.update(len(response_content))
            return start, response_content

        def _save_to_file(outpath, stream_data):
            with open(outpath, 'wb') as f:
                for start, content in stream_data:
                    f.seek(start)
                    f.write(content)

        if self.is_live:
            self._process_error(er_type='download',
                                data={'url': self.url, 'reason': "Can't download livestream", 'is_fatal': False,
                                      'message': f"Can't download livestream"})
            return
        for j in range(2):
            headers = {}
            headers.update(self._client_info['headers'].copy())
            if j > 0 and 'Authorization' in self._headers:
                del self._headers['Authorization']
            headers.update(self._headers)
            for i in range(len(AVAILABLE_CLIENTS)):
                stream = self._get_stream(quality=quality, only_audio=only_audio, only_video=only_video,
                                          target_fps=target_fps, itag=target_itag)
                download_url = stream.get('url')

                response = requests.get(download_url, stream=True, headers=headers)
                status = response.status_code
                if status == 200 or self._no_retry:
                    break
                else:
                    self._client = AVAILABLE_CLIENTS[i]
                    self._client_info = CLIENT_INFO[self._client]
                    self._extract_video_info(i, skip_on_error=True)
                    self._get_data()
            else:
                if status == 200 or self._no_retry:
                    break

        if status == 403:
            self._process_error(er_type="forbidden", data={'url': self.url, 'is_fatal': False})
            return
        elif status != 200:
            self._process_error(er_type="download", data={'url': self.url, 'is_fatal': False,
                                         'reason': f'Unsuccessful request - Code <{status}> | {response.reason}'})
            return

        dir_path = os.path.abspath(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        self._send_info_message(f"Downloading stream - itag: {stream.get('itag')}")
        total_size = int(response.headers.get('content-length', 0))
        raw_path = os.path.join(path, f"temp_{_raw_number}.raw")

        with open(raw_path, 'wb') as f:
            f.truncate(total_size)

        ranges = [(i, min(i + chunk_size - 1, total_size - 1)) for i in range(0, total_size, chunk_size)]
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(_download_chunk, download_url, start, end, pbar) for start, end in ranges]
                downloaded_data = [future.result() for future in futures]

        download_title = _format_title(self.title) if self.title else "download"
        ext = preferred_audio_format if only_audio else preferred_video_format
        output_path = os.path.join(path, download_title+"."+ext)

        if not force_ffmpeg:
            _save_to_file(output_path, downloaded_data)
            self._send_success_message(f"Successfully downloaded `{self.title}` into {dir_path}.")
            """with open(raw_path, "wb") as f, tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                    for data in response.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        pbar.update(len(data))
    
                
    
                if not force_ffmpeg:
                    with open(output_path, 'wb') as wfile:
                        with open(raw_path, "rb") as f:
                            wfile.write(f.read())"""
        else:
            command = ['ffmpeg', '-y', '-i', raw_path, output_path]
            try:
                with tqdm(total=100, desc="Converting with ffmpeg") as pbar:
                    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
                    for line in process.stderr:
                        if "time=" in line:
                            time_str = re.search(r"time=(\d+:\d+:\d+\.\d+)", line)
                            if not time_str:
                                continue
                            time_str = time_str.group(1)
                            current_time = sum(int(x) * 60 ** (i-1) for i, x in enumerate(reversed(re.split(r'[:.]', time_str))))
                            progress = 100*current_time / self._duration
                            pbar.last_print_n = progress
                            pbar.update()
            except subprocess.CalledProcessError as e:
                print(_red(e))

        os.remove(raw_path)

    def _get_stream(self, quality="best", only_audio=False, only_video=False, target_fps=-1, itag=-1):

        video_formats = audio_formats = ["mp4", "webm"]
        streams = self._get_streams()
        if not streams:
            self._process_error(er_type='download',
                                data={'url': self.url, 'reason': "No streams available", 'is_fatal': False,
                                      'message': f"No streams available"})
            return
        formats = streams.get('adaptiveFormats') if only_audio or only_video else streams.get('formats')
        if not formats:
            st_url = {'url': streams.get('hlsUrl')}
            if st_url.get('url'): return st_url
            self._process_error(er_type='download',
                                data={'url': self.url, 'reason': "Couldn't get formats",
                                      'is_fatal': False, 'message': f"Couldn't get formats"})
            return
        streams_sorted = sorted(formats, key=lambda x: x['bitrate'], reverse=True)

        download_stream = None
        filtered_streams = []
        excluded_itags = {}
        if itag < 0:
            if only_audio:
                audio_formats = ["audio/" + ext for ext in audio_formats]
                for stream in streams_sorted:
                    mtype = stream.get('mimeType')
                    if not mtype or not mtype.split("; ")[0] in audio_formats or stream.get(
                        'itag') in excluded_itags: continue
                    filtered_streams.append(stream)
            else:
                if target_fps and target_fps > 0:
                    streams_sorted = sorted(formats, key=lambda x: (x['fps'] if 'fps' in x else 0, x['bitrate']),
                                            reverse=True)
                video_formats = ["video/" + ext for ext in video_formats]
                fps_set = set()
                for stream in streams_sorted:
                    mtype = stream.get('mimeType')
                    if not mtype or not mtype.split("; ")[0] in video_formats or stream.get('itag') in excluded_itags: continue
                    filtered_streams.append(stream)
                    fps_set.add(stream.get('fps'))
                fps = min(fps_set, key=lambda x: abs(x - target_fps))
            stream_index = 0
            formats_length = len(filtered_streams) - 1
            if quality in LOWEST_KEYWORDS:
                stream_index = -1
                if target_fps and target_fps > 0:
                    for i, stream in enumerate(filtered_streams.__reversed__()):
                        stream_fps = stream.get('fps')
                        if not stream_fps:
                            continue
                        if stream_fps == fps:
                            stream_index = i - 1
            elif quality in LOW_KEYWORDS:
                stream_index = formats_length // 4
            elif quality in MEDIUM_KEYWORDS:
                stream_index = formats_length // 2
            elif quality in HIGH_KEYWORDS:
                stream_index = 3 * formats_length // 4
            else:
                if target_fps and target_fps > 0:
                    for i, stream in enumerate(filtered_streams):
                        stream_fps = stream.get('fps')
                        if not stream_fps:
                            continue
                        if stream_fps == fps:
                            stream_index = i - 1
            download_stream = filtered_streams[stream_index]
        else:
            for stream in streams_sorted:
                if stream.get('itag') == itag:
                    download_stream = stream
                    break
            if not download_stream:
                download_stream = streams_sorted[0]
        if not download_stream:
            self._process_error(er_type='download',
                                data={'url': self.url, 'reason': "Couldn't get stream",
                                      'is_fatal': False, 'message': f"Couldn't get stream"})
            return
        return download_stream

    def _get_streams(self):
        format_info = {
            'formats': [],
            'adaptiveFormats': [],
            'dashUrl': None,
            'hlsUrl': None
        }

        formats = self.streaming_data.get('formats')
        if formats:
            for format in formats:
                format_info['formats'].append(format)
        adaptive_formats = self.streaming_data.get('adaptiveFormats')
        if adaptive_formats:
            for format in adaptive_formats:
                format_info['adaptiveFormats'].append(format)

        dash_url = self.streaming_data.get('dashManifestUrl')
        if dash_url:
            format_info['dashUrl'] = dash_url
        hls_url = self.streaming_data.get('hlsManifestUrl')
        if hls_url:
            format_info['hlsUrl'] = hls_url

        return format_info

    def _get_headers(self, access_token):
        if self._use_login: YOUTUBE_HEADERS.update({
                            'Authorization': f'Bearer {access_token}'
                        })
        return YOUTUBE_HEADERS

    def _get_token(self):
        if not self._disable_cache and os.path.exists(ACCESS_TOKEN_DIR):
            with open(ACCESS_TOKEN_DIR, 'r') as f:
                access_token = json.load(f).get('access_token')
            return access_token

        response = requests.post('https://oauth2.googleapis.com/device/code',
                                 data={'client_id': CLIENT_ID,'scope': 'https://www.googleapis.com/auth/youtube'})

        response_data = response.json()
        self._send_info_message("Logging in...", ignore_verbose=True)
        self._send_info_message(f"Open {response_data.get('verification_url')} and use the code {response_data.get('user_code')}", ignore_verbose=True)
        input(_dim_cyan("[INFO]: Press enter when completed."))

        response = requests.post('https://oauth2.googleapis.com/token',
            data={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'device_code': response_data['device_code'], 'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'})
        response_data = response.json()

        return self._write_cache(response_data['access_token'])

    def _write_cache(self, token):
        if self._disable_cache:
            return token
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        with open(ACCESS_TOKEN_DIR, 'w') as f:
            json.dump({'access_token': token}, f)
        return token

    def _search_query(self):
        url = "https://www.youtube.com/results?search_query=" + self._query
        html = requests.get(url, headers=self._headers).text

        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', string=re.compile(r'var ytInitialData'))
        if not script_tag:
            return

        json_text = re.search(r'var ytInitialData = ({.*?});', script_tag.string, re.DOTALL).group(1)
        keys = ['contents', 'twoColumnSearchResultsRenderer', 'primaryContents', 'sectionListRenderer', 'contents', 0, 'itemSectionRenderer', 'contents']
        try:
            contents = json.loads(json_text)
            for key in keys:
                contents = contents[key]
        except:
            self._process_error(er_type="extract",
                                data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                      'reason': "Couldn't get json data"})
        for vid_info in contents:
            if 'videoRenderer' in vid_info:
                return vid_info.get('videoRenderer').get('videoId')
        return

    def _extract_video_info(self, attempt=0, skip_on_error=False):
        if attempt == 0: self._send_info_message(f"Trying extraction with {self._client}")
        self._client_info['payload'].update({
            "videoId": self.video_id
        })
        headers = self._headers.copy()
        headers.update({
            'Content-Type': 'application/json',
        })
        headers.update(self._client_info['headers'].copy())
        req = requests.post(f'https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8', headers=headers, json=self._client_info['payload'])
        if req.status_code == 200:
            data = req.json()
        else:
            req = requests.get(self.url, headers=self._headers)
            if req.status_code != 200:
                self._process_error(er_type="extract",
                                    data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                          'reason': f'Unsuccessful request - Code <{req.status_code}> | {req.reason}'})
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            script_tag = soup.find("script", string=re.compile('ytInitialPlayerResponse'))
            if not script_tag:
                self._process_error(er_type="extract",
                                    data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                          'reason': f"Couldn't get ytInitialPlayerResponse"})

            json_text = re.search(r'var ytInitialPlayerResponse = ({.*?});', script_tag.string, re.DOTALL).group(1)
            data = json.loads(json_text)

        tmp_pl = data.get('playabilityStatus')
        playability_status = tmp_pl.get('status') if tmp_pl else None
        if playability_status is None or playability_status == 'ERROR' and not skip_on_error:
            self._process_error(er_type="extract",
                                data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                      'reason': 'Video Unavailable (Invalid URL or removed video)'})
        elif playability_status == 'LOGIN_REQUIRED' and not skip_on_error:
            reason = tmp_pl.get("reason")
            if not reason:
                try:
                    reason = tmp_pl.get('errorScreen').get('playerErrorMessageRenderer').get('subreason').get('simpleText')
                except:
                    reason = "Unknown"
            self._process_error(er_type="extract",
                                data={'url': self.url, 'extract_type': 'video info', 'is_fatal': False,
                                      'reason': f'This video is private - {reason}',
                                      'message': f'This video is private - {reason}'})

        if 'streamingData' not in data and not self._no_retry:
            if attempt >= len(AVAILABLE_CLIENTS) - 1:
                return {}
            prev = self._client
            self._client = AVAILABLE_CLIENTS[attempt+1]
            self._client_info = CLIENT_INFO[self._client]
            self._send_info_message(f"Extraction failed with {prev}. Retrying with {self._client}")
            data = self._extract_video_info(attempt=attempt+1)

        return data

    def _process_error(self, er_type, data):
        is_fatal = data.get('is_fatal')
        if self._ignore_errors and not is_fatal:
            if not self._ignore_warnings:
                print(_dim_yellow("[WARNING]: " + data.get('message')))
        else:
            if er_type == 'warning' and not self._ignore_warnings:
                print(_dim_yellow("[WARNING]: " + data.get('message')))
            elif er_type == "search":
                raise SearchError(query=data.get('query'))
            elif er_type == "extract":
                raise ExtractError(url=data.get('url'), reason=data.get('reason'), extract_type=data.get('extract_type'))
            elif er_type == "download":
                raise DownloadError(url=data.get('url'), reason=data.get('reason'))
            elif er_type == "forbidden":
                raise ForbiddenError(url=data.get('url'))

    def _send_info_message(self, message, ignore_verbose=False):
        if self._verbose or ignore_verbose:
            print(_dim_cyan("[INFO]: "+message))

    def _send_success_message(self, message):
        if self._verbose:
            print(_green("[SUCCESS]: "+message))

    def __str__(self):
       return f"<youtube_extractor.__main__.Video object with url={self.url}>"

    def __dir__(self):
        """
        Modified dir() to display only common use methods.

        To see the complete dir, use Video().__default_dir__()
        """
        default_dir = super().__dir__()
        return [attribute for attribute in default_dir if not attribute.startswith("_")]

    def __default_dir__(self):
        return super().__dir__()


class Search:
    """
    Search the given query and fetch the results.
    Automatically get the Video class for each result or only get simple information (title, url, duration, ...).

    Attributes
    ----------
    query: str
        A query to search for
    get_simple: bool (False)
        Get only simplified data of the video (to save time in case the stream/download isn't required)
    use_threads: bool (True)
        Obtain the information/download the videos using threads (parallel processing)
    threads: int (Half of the available threads)
        Amount of threads to use
    download_kwargs: dict (Default parameters)
        The arguments to parse to the `download` method, inherited from `Video.download()`
    kwargs: dict (Default parameters)
        Inherits `Video` kwargs

    Methods
    -------
    download(**kwargs)
        Inherits `Video.download()` arguments
    """
    def __init__(self, query, get_simple=False, use_threads=True, threads=os.cpu_count()//2, max_duration=-1, **kwargs):
        """Make a Search class.

        :param str query:
            A query to search for
        :param bool get_simple:
            Get only simplified data of the video (to save time in case the stream/download isn't required):
            title, video id, url, duration, views, channel name/url/id
        :param bool use_threads:
            Obtain the information/download the videos using threads (parallel processing)
        :param int threads:
            Amount of threads to use
        :param dict download_kwargs:
            The arguments to parse to the `download` method, inherited from `Video.download()`
        :param dict kwargs:
            Inherits `Video` kwargs
        :param int max_duration:
            Max duration of a video, in seconds
        """
        kwargs.setdefault('ignore_errors', True)
        kwargs.setdefault('ignore_warnings', True)
        kwargs.setdefault('verbose', False)
        self._ignore_errors = kwargs.get('ignore_errors')
        self._ignore_warnings = kwargs.get('ignore_warnings')
        self._verbose = kwargs.get('verbose')
        self._headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        self._max_dur = max_duration
        self.results = None
        self._query = query.strip()
        self.videos_info = self._search_query()
        self.video_urls = list(filter(None, [vid.get('url') for vid in self.videos_info]))
        if not self.video_urls:
            self._process_error(er_type="search", data={'query': query, 'is_fatal': True})
        if get_simple:
            return

        self._kwargs = kwargs
        self._download_kwargs = {}
        self._threads = threads
        self._use_threads = use_threads
        if self._use_threads:
            with ThreadPoolExecutor(max_workers=self._threads) as executor:
                results = list(executor.map(self._get_info, self.video_urls))
        else:
            results = []
            for url in self.video_urls:
                results.append(Video(url, **self._kwargs))
        self.results = results

    def download(self, **download_wargs):
        """
        Inherits `Video.download()` arguments
        """
        self._download_kwargs.update(download_wargs)
        if self.results is None:
            self._process_error(er_type="download", data={'url': self._query, 'is_fatal': False,
                                            'reason': f'No results found (have you set get_only_urls=True?)'})
            return

        if self._use_threads:
            with ThreadPoolExecutor(max_workers=self._threads) as executor:
                executor.map(self._download_vids, self.results, [i for i in range(len(self.results))])
        else:
            for vid in self.results:
                vid.download(**self._download_kwargs)

    def _get_info(self, url):
        return Video(url, **self._kwargs)

    def _download_vids(self, vid, number):
        self._download_kwargs.update({
            "_raw_number": number
        })
        vid.download(**self._download_kwargs)

    def _search_query(self):
        url = "https://www.youtube.com/results?search_query=" + self._query
        html = requests.get(url, headers=self._headers).text

        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find('script', string=re.compile(r'var ytInitialData'))
        if not script_tag:
            return

        json_text = re.search(r'var ytInitialData = ({.*?});', script_tag.string, re.DOTALL).group(1)
        keys = ['contents', 'twoColumnSearchResultsRenderer', 'primaryContents', 'sectionListRenderer', 'contents', 0, 'itemSectionRenderer', 'contents']
        try:
            contents = json.loads(json_text)
            for key in keys:
                contents = contents[key]
        except:
            self._process_error(er_type="extract",
                                data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                      'reason': "Couldn't get json data"})

        videos_info = []
        for vid in contents:
            if 'videoRenderer' in vid:
                vid_info = vid.get('videoRenderer')
                video_id = str(vid_info.get('videoId'))
                url = "https://www.youtube.com/watch?v="+video_id
                if url == "https://www.youtube.com/watch?v=None": continue
                thumbnail, title = vid_info.get('thumbnail', {}).get('thumbnails')[-1], \
                                   vid_info.get('title', {}).get('runs', {})[0].get('text')
                fduration, views = vid_info.get('lengthText', {}).get('simpleText'), \
                                  re.sub(r'( views|,)', '', vid_info.get('viewCountText', {}).get('simpleText', 'none'))
                duration, fviews = formatted_to_seconds(fduration), _format_views(views)
                if self._max_dur > 0 and duration > self._max_dur:
                    continue
                ch = vid_info.get('longBylineText', {}).get('runs')[0]
                channel, channel_id = ch.get('text'), \
                                      ch.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                channel_url = "https://www.youtube.com/channel/"+channel_id
                videos_info.append({
                    'title': title, 'video_id': video_id, 'url': url, 'duration': duration, 'fduration': fduration,
                    'views': None if views == 'none' else int(views), 'fviews': fviews, 'channel': channel, 'channel_url': channel_url,
                    'channel_id': channel_id
                })
        return videos_info

    def _process_error(self, er_type, data):
        is_fatal = data.get('is_fatal')
        if self._ignore_errors and not is_fatal:
            if not self._ignore_warnings:
                print(_dim_yellow("[WARNING]: " + data.get('message')))
        else:
            if er_type == 'warning' and not self._ignore_warnings:
                print(_dim_yellow("[WARNING]: " + data.get('message')))
            elif er_type == "search":
                raise SearchError(query=data.get('query'))
            elif er_type == "extract":
                raise ExtractError(url=data.get('url'), reason=data.get('reason'), extract_type=data.get('extract_type'))
            elif er_type == "download":
                raise DownloadError(url=data.get('url'), reason=data.get('reason'))
            elif er_type == "forbidden":
                raise ForbiddenError(url=data.get('url'))

    def _send_info_message(self, message):
        if self._verbose:
            print(_dim_cyan("[INFO]: "+message))

    def __str__(self):
       return f"<youtube_extractor.__main__.Search object with query={self._query}>"

    def __dir__(self):
        """
        Modified dir() to display only common use methods.

        To see the complete dir, use Video().__default_dir__()
        """
        default_dir = super().__dir__()
        return [attribute for attribute in default_dir if not attribute.startswith("_")]

    def __default_dir__(self):
        return super().__dir__()


class Playlist:
    # TODO
    def __init__(self):
        raise NotImplementedError("Playlists are not yet implemented.")
