import io
import os
import json
import re
import subprocess
import warnings

import requests

from concurrent.futures import ThreadPoolExecutor
from typing import List, Union, Tuple, Dict, Iterable

from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from colorama import just_fix_windows_console
from tqdm import tqdm

from .utils import (CACHE_DIR, ACCESS_TOKEN_DIR, CLIENT_ID, CLIENT_SECRET, CLIENT_INFO, AVAILABLE_CLIENTS,
                    YOUTUBE_HEADERS, LOWEST_KEYWORDS, LOW_KEYWORDS, MEDIUM_KEYWORDS, HIGH_KEYWORDS,
                    _format_date, _format_views, format_seconds, formatted_to_seconds, _format_title,
                    _get_chapters, _get_channel_picture, _is_valid_yt_url, _convert_captions, _send_warning_message,
                    _send_info_message, _send_success_message, _process_error, _from_short_number, _to_short_number)
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
        no_retry: bool (False) - Disable retries in case extraction/download fails with the set client.
        client: str ("android_embed") - Client to use. ("android_embed", "android_music", "tv_embed", "ios", "android", "android_creator", "web", "ios_embed")

    Methods
    -------
    download(path: str = ".", quality: str = "best", keep: bool = False, only_audio: bool = False,
             only_video: bool = False, target_fps: int = -1, target_itag: int = -1,
             preferred_video_format: str = "mp4", preferred_audio_format: str = "mp3", chunk_size: int = 1024*1024,
             force_ffmpeg: bool = False)
        Downloads an appropriate video/audio stream.

        path: str - Output path.
        quality: str - Quality of the stream (by bitrate): "best", "high", "med", "low", "lowest".
        keep: bool - Keep the audio and video files (in case they exist).
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
            "max_comments": 60,
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
        self._clients_used = set()
        self._change_client(client=parameters.get("client").lower(), headers=None)
        if invalid_params:
            _send_warning_message(f"The following parameters aren't valid: {', '.join(invalid_params)}", self._ignore_warnings)

        if not query:
            _process_error(er_type="noquery", data={'is_fatal': True},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        self._query = query.strip()

        self._use_login = parameters.get("use_login")
        self._disable_cache = parameters.get("disable_cache")
        access_token = None
        if parameters.get("use_login"):
            access_token = self._get_token()
        self._headers = self._get_headers(access_token=access_token)

        is_valid_url = _is_valid_yt_url(self._query)

        self.video_id = self._search_query() if is_valid_url[1] is None else is_valid_url[1]
        if self.video_id is None:
            _process_error(er_type="search", data={'query': query, 'is_fatal': True},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        elif not self.video_id:
            self.url = self._query
        else:
            self.url = "https://www.youtube.com/watch?v="+self.video_id
        self.json = self._extract_video_info()

        self._max_comments = parameters.get("max_comments", 60)
        self._params = parameters
        self._get_data()

    def _get_data(self):
        parameters = self._params
        couldnt_extract = []
        self.video_info = self.json.get('videoDetails', {})
        if not self.video_info:
            _process_error(er_type="extract",
                                data={'url': self.url, 'reason': '',
                                      'extract_type': 'video details (title, length, ...)',
                                      'message': f"Couldn't extract video details (title, length, ...) for {self.url}",
                                      'is_fatal': False},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        self.streaming_data = self.json.get('streamingData', {})
        if not self.streaming_data:
            _process_error(er_type="extract",
                                data={'url': self.url, 'reason': '', 'extract_type': 'streaming data',
                                      'message': f"Couldn't extract streaming data for {self.url}", 'is_fatal': False},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
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
        if couldnt_extract:
            _send_warning_message(f"Couldn't extract {', '.join(couldnt_extract)} for {self.url}", self._ignore_warnings)

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
        views = int(self.video_info.get('viewCount', -1))
        self.views = _format_views(str(views)) if parameters.get("get_views_formatted") else views
        self.is_live = bool(self.video_info.get('isLiveContent', False))
        self.streams = None
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

    def download(self, path: str = ".", quality: str = "best", keep: bool = False, only_audio: bool = False,
                 only_video: bool = False, target_fps: int = -1, target_itag: int = -1,
                 preferred_video_format: str = "mp4", preferred_audio_format: str = "mp3", chunk_size: int = 1024*1024,
                 force_ffmpeg: bool = False, _raw_number=0, _show_bar=True):
        """
        Downloads an appropriate video/audio stream.

        Args:
        - path [str]: Output path. Defaults to the current directory.
        - quality [str]: Quality of the stream (by bitrate): "best", "high", "med", "low", "lowest". Defaults to "best".
        - keep [bool]: Keep the audio and video files (in case they exist). Defaults to False.
        - only_audio [bool]: Gets a stream with only audio data. Defaults to False.
        - only_video [bool]: Gets a stream with only video data. Defaults to False.
        - target_fps [int]: Target fps of the video, preferred over bitrate. Defaults to -1 (ignore fps, order by bitrate).
        - target_itag [int]: Target itag of the stream to download. Defaults to -1 (no specific itag).
        - preferred_video_format [str]: Video format to download into. Defaults to "mp4".
        - preferred_audio_format [str]: Audio format to download into (for only_audio=True). Defaults to "mp3".
        - chunk_size [int]: Size of the chunks to download. Increase if you're experiencing low speeds, decrease if you want to limit. Defaults to 1024*1024.
        - force_ffmpeg [bool]: Force the conversion to bytes to be made using ffmpeg, use it for format conversion. Defaults to False.
        """
        if self.is_live:
            _process_error(er_type='download',
                                data={'url': self.url, 'reason': "Can't download livestream", 'is_fatal': False,
                                      'message': f"Can't download livestream"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return

        check = True
        while check:
            stream = self._get_stream(quality=quality, only_audio=only_audio, only_video=only_video,
                                      target_fps=target_fps, itag=target_itag)
            download_url = stream.get('url')

            response = requests.get(download_url, stream=True, headers=self._headers)
            status = response.status_code

            if status == 200 or self._no_retry:
                break
            else:
                check = self._change_client()
                self.json = self._extract_video_info(silent=True, skip_on_error=True)
                self._get_data()

        if status == 403:
            _process_error(er_type="forbidden", data={'url': self.url, 'is_fatal': False},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return
        elif status != 200:
            _process_error(er_type="download", data={'url': self.url, 'is_fatal': False,
                                         'reason': f'Unsuccessful request - Code <{status}> | {response.reason}'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return
        elif not download_url:
            _process_error(er_type="download", data={'url': self.url, 'is_fatal': False,
                                                     'reason': f"Couldn't find stream url"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return

        dir_path = os.path.abspath(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        itags = [str(stream.get('itag'))]
        exts = [preferred_audio_format if only_audio else preferred_video_format]
        stream_urls = [download_url]
        total_sizes = [int(response.headers.get('content-length', 0))]
        if not only_video and not only_audio and itags[0] not in {'18', '22'}:
            audio_stream = self._get_stream(quality=quality, only_audio=True, only_video=False, itag=target_itag)
            video_stream = self._get_stream(quality=quality, only_audio=False, only_video=True, target_fps=target_fps, itag=target_itag)
            itags = ["a:"+str(audio_stream.get('itag')), "v:"+str(video_stream.get('itag'))]
            exts = [preferred_audio_format, preferred_video_format]
            stream_urls = [audio_stream.get('url'), video_stream.get('url')]

            audio_response = requests.get(stream_urls[0], stream=True, headers=self._headers)
            video_response = requests.get(stream_urls[1], stream=True, headers=self._headers)

            total_sizes = [int(audio_response.headers.get('content-length', 0)),
                           int(video_response.headers.get('content-length', 0))]

        pl = 's' if len(itags) > 1 else ''
        _send_info_message(f"Downloading stream{pl} - itag{pl}: {'+'.join(itags)}", verbose=self._verbose)
        if len(stream_urls) > 1:
            raw_paths = [os.path.join(path, f"temp_{_raw_number}_{preferred_audio_format}_{itags[0].replace(':', '')}.raw"),
                         os.path.join(path, f"temp_{_raw_number}_{preferred_video_format}_{itags[1].replace(':', '')}.raw")]
        else:
            raw_paths = [os.path.join(path, f"temp_{_raw_number}.raw")]

        data_to_download = []
        for d in zip(stream_urls, exts, itags, total_sizes):
            data_to_download.append((d[0], d[1], d[2], d[3]))
        download_title = _format_title(self.title) if self.title else "download"
        output_path = os.path.join(path, download_title + "_")

        self._download_streams(download_urls=data_to_download, chunk_size=chunk_size, raw_paths=raw_paths,
                               output_path=output_path, force_ffmpeg=force_ffmpeg, show_bar=_show_bar)

        if len(stream_urls) > 1:
            exts2 = [itags[0].replace(":", "")+".", itags[1].replace(":", "")+"."]
            self._combine_av(output_path+exts2[0]+exts[0], output_path+exts2[1]+exts[1], output_path[:-1]+"."+exts[1])
            if not keep:
                if os.path.exists(output_path+exts2[0]+exts[0]):
                    os.remove(output_path+exts2[0]+exts[0])
                if os.path.exists(output_path+exts2[1]+exts[1]):
                    os.remove(output_path+exts2[1]+exts[1])

            _send_success_message(f"Merged audio (itag: {audio_stream.get('itag')}) and video (itag: {video_stream.get('itag')}).", self._verbose)
        else:
            try:
                os.rename(output_path + itags[0] + "." + exts[0], output_path[:-1] + "." + exts[0])
            except:
                pass

        _send_success_message(f"Successfully downloaded `{self.title}` into `{dir_path}`.", verbose=self._verbose)

    def _download_streams(self, download_urls, chunk_size, raw_paths, output_path, force_ffmpeg=False, show_bar=True):
        def _download_chunk(url, start, end, session, pbar):
            response_content = session.get(url, headers={'Range': f'bytes={start}-{end}'}, stream=True).content
            if pbar: pbar.update(len(response_content))
            return start, response_content

        i = 0
        for download_url, ext, ext2, total_size in download_urls:
            with open(raw_paths[i], 'wb') as f:
                f.truncate(total_size)

            ranges = [(i, min(i + chunk_size - 1, total_size - 1)) for i in range(0, total_size, chunk_size)]
            pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") if show_bar else None
            with ThreadPoolExecutor(max_workers=8) as executor:
                with requests.Session() as session:
                    futures = [executor.submit(_download_chunk, download_url, start, end, session, pbar) for start, end in ranges]
                    downloaded_data = [future.result() for future in futures]

            self._save_to_file(output_path=output_path, ext=ext, ext2=ext2.replace(":", "")+".", raw_path=raw_paths[i],
                               stream_data=downloaded_data, force_ffmpeg=force_ffmpeg)

            i += 1

    def _save_to_file(self, output_path, ext, ext2='', raw_path=None, stream_data=None, force_ffmpeg=False):
        with open(output_path + ext2 + ext, 'wb') as f:
            for start, content in stream_data:
                f.seek(start)
                f.write(content)
        if force_ffmpeg:
            try:
                subprocess.run(['ffmpeg', '-y', '-i', output_path + ext2 + ext, output_path +"_ffmpeg_"+ ext2 + ext])
                os.remove(output_path + ext2 + ext)
            except Exception as e:
                pass
                #_process_error()

        if os.path.exists(raw_path):
            os.remove(raw_path)

    @staticmethod
    def _combine_av(audio_path, video_path, output_path):
        try:
            # Change to pbar
            _send_info_message("Converting...", self._verbose)
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', output_path])
        except Exception as e:
            print(_red(e))

    def _get_stream(self, quality="best", only_audio=False, only_video=False, target_fps=-1, itag=-1):

        video_formats = audio_formats = ["mp4", "webm"]
        self.streams = streams = self._get_streams()
        if not streams:
            _process_error(er_type='download',
                                data={'url': self.url, 'reason': "No streams available", 'is_fatal': False,
                                      'message': f"No streams available"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return {}
        formats = streams.get('adaptiveFormats') if only_audio or only_video else streams.get('formats')

        if not formats:
            formats = streams.get('adaptiveFormats')
            if not formats:
                st_url = {'url': streams.get('hlsUrl')}
                if st_url.get('url'): return st_url
                _process_error(er_type='download',
                                    data={'url': self.url, 'reason': "Couldn't get formats",
                                          'is_fatal': False, 'message': f"Couldn't get formats"},
                               ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
                return {}
        streams_sorted = sorted(formats, key=lambda x: x['bitrate'], reverse=True)

        download_stream = None
        filtered_streams = []
        #excluded_video_itags = {140, 137, 136, 135, 134, 133, 160}
        excluded_video_itags = {}
        excluded_audio_itags = {}
        if itag < 0:
            if only_audio:
                audio_formats = ["audio/" + ext for ext in audio_formats]
                for stream in streams_sorted:
                    mtype = stream.get('mimeType')
                    if not mtype or not mtype.split("; ")[0] in audio_formats or stream.get('itag') in excluded_audio_itags: continue
                    filtered_streams.append(stream)
            else:
                if target_fps and target_fps > 0:
                    streams_sorted = sorted(formats, key=lambda x: (x['fps'] if 'fps' in x else 0, x['bitrate']),
                                            reverse=True)
                video_formats = ["video/" + ext for ext in video_formats]
                fps_set = set()
                for stream in streams_sorted:
                    mtype = stream.get('mimeType')
                    if not mtype or not mtype.split("; ")[0] in video_formats or stream.get('itag') in excluded_video_itags: continue
                    filtered_streams.append(stream)
                    fps_set.add(stream.get('fps'))
                if not filtered_streams:
                    _process_error(er_type='download',
                                   data={'url': self.url, 'reason': "Couldn't get formats",
                                         'is_fatal': False, 'message': f"Couldn't get formats"},
                                   ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
                    return {}
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
            _process_error(er_type='download',
                                data={'url': self.url, 'reason': "Couldn't get stream",
                                      'is_fatal': False, 'message': f"Couldn't get stream"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return {}
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
                if not format.get('url'):
                    continue
                format_info['formats'].append(format)
        adaptive_formats = self.streaming_data.get('adaptiveFormats')
        if adaptive_formats:
            for format in adaptive_formats:
                if not format.get('url'):
                    continue
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
        _send_info_message("Logging in...", ignore_verbose=True, verbose=self._verbose)
        _send_info_message(f"Open {response_data.get('verification_url')} and use the code {response_data.get('user_code')}", ignore_verbose=True, verbose=self._verbose)
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

    def _change_client(self, client=None, headers={}):
        if client and not client in self._clients_used:
            self._client = client
        else:
            self._client = None
            for _client in AVAILABLE_CLIENTS:
                if _client not in self._clients_used:
                    self._client = _client
                    break
            if not self._client:
                return False
        self._client_info = CLIENT_INFO[self._client].copy()
        if headers is None:
            self._headers = {}
        self._headers.update(self._client_info['headers'].copy())
        self._clients_used.add(self._client)
        return True

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
            _process_error(er_type="extract",
                                data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                      'reason': "Couldn't get json data"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        for vid_info in contents:
            if 'videoRenderer' in vid_info:
                return vid_info.get('videoRenderer').get('videoId')
        return

    def _extract_video_info(self, silent=False, skip_on_error=False):
        if not silent:
            _send_info_message(f"Trying extraction with {self._client}", verbose=self._verbose)

        payload = self._client_info['payload'].copy()
        payload.update({
            "videoId": self.video_id
        })
        headers = self._headers.copy()
        headers.update({
            'Content-Type': 'application/json',
        })
        headers.update(self._client_info['headers'].copy())

        req = requests.post(f'https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
                            headers=headers, json=payload)


        if req.status_code == 200:
            data = req.json()
        else:
            req = requests.get(self.url, headers=self._headers)
            if req.status_code != 200:
                _process_error(er_type="extract",
                                    data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                          'reason': f'Unsuccessful request - Code <{req.status_code}> | {req.reason}'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            script_tags = soup.find_all("script", string=re.compile('ytInitialPlayerResponse'))
            script_tag = None
            for tag in script_tags:
                if "var ytInitialPlayerResponse = null" not in str(tag):
                    script_tag = tag
                    break
            if not script_tag:
                _process_error(er_type="extract",
                                    data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                          'reason': f"Couldn't get ytInitialPlayerResponse"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)

            json_text = re.search(r'var ytInitialPlayerResponse = ({.*?});', script_tag.string, re.DOTALL).group(1)
            data = json.loads(json_text)

        tmp_pl = data.get('playabilityStatus')
        playability_status = tmp_pl.get('status') if tmp_pl else None

        if playability_status is None or playability_status == 'ERROR' and not skip_on_error:
            prev = self._client
            check = self._change_client()
            if check and not self._no_retry:
                _send_info_message(f"Extraction failed with {prev}. Retrying with {self._client}", verbose=self._verbose)
                data = self._extract_video_info(silent=True)
            else:
                _process_error(er_type="extract",
                                    data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                          'reason': 'Video Unavailable (Invalid URL or removed video)'},
                               ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        elif playability_status in {'LOGIN_REQUIRED', 'UNPLAYABLE'} and not skip_on_error:
            prev = self._client
            check = self._change_client(client="tv_embed" if not self._use_login else None)
            if check and not self._no_retry:
                _send_info_message(f"Extraction failed with {prev}. Retrying with {self._client}", verbose=self._verbose)
                data = self._extract_video_info(silent=True)
            else:
                reason = tmp_pl.get("reason")
                if not reason:
                    try:
                        reason = tmp_pl.get('errorScreen').get('playerErrorMessageRenderer').get('subreason').get('simpleText')
                    except:
                        reason = "Unknown"
                _process_error(er_type="extract",
                                    data={'url': self.url, 'extract_type': 'video info', 'is_fatal': False,
                                          'reason': f'This video is private - {reason}',
                                          'message': f'This video is private - {reason}'},
                               ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        if 'streamingData' not in data and not self._no_retry:
            prev = self._client
            check = self._change_client()
            if not check:
                return {}

            _send_info_message(f"Extraction failed with {prev}. Retrying with {self._client}", verbose=self._verbose)
            data = self._extract_video_info(silent=True)

        return data

    @property
    def comments(self):
        session = requests.Session()
        req = session.get(self.url, headers=self._headers)
        if req.status_code != 200:
            _process_error(er_type="extract", data={'url': self.url, 'is_fatal': True,
                                                    'extract_type': 'comment contents',
                                                    'reason': f'Unsuccessful request - Code <{req.status_code}> | {req.reason}'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find("script", string=re.compile('ytInitialData'))

        json_text = re.search(r'var ytInitialData = ({.*?});', script_tag.string, re.DOTALL).group(1)
        data = json.loads(json_text)
        contents = data.get('contents', {}).get('twoColumnWatchNextResults', {}).get('results', {}).get('results', {}).get('contents', [{}, {}, {}, {}])
        target_id = contents[3].get('itemSectionRenderer', {}).get('targetId')
        ctoken = contents[3].get('itemSectionRenderer', {}).get('contents', [{}])[0].get('continuationItemRenderer', {}).get('continuationEndpoint', {}).get('continuationCommand', {}).get('token')
        comments = []
        i = 1

        while ctoken:
            base_url = "https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
            payload = CLIENT_INFO['web']['payload'].copy()
            payload.update({
                'continuation': ctoken,
                'targetId': target_id
            })
            response = session.post(base_url, headers=CLIENT_INFO['web']['headers'], json=payload)
            if response.status_code != 200:
                _process_error(er_type="extract", data={'url': self.url, 'is_fatal': False,
                                                        'extract_type': 'comment contents',
                                                        'reason': f'Unsuccessful request - Code <{response.status_code}> | {response.reason}'},
                               ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            data = response.json()
            comments_data = data.get('frameworkUpdates', {}).get('entityBatchUpdate', {}).get('mutations', [])
            for comment_info in comments_data:
                comment = comment_info.get('payload', {}).get('commentEntityPayload')
                if comment:
                    if i > self._max_comments:
                        return comments
                    owner = comment.get('author')
                    author_id = owner.get('channelId')
                    properties = comment.get('properties')
                    toolbar = comment.get('toolbar')
                    likes = _from_short_number(toolbar.get('likeCountNotliked', '0'))
                    dislikes = abs(_from_short_number(toolbar.get('likeCountLiked', '0')) - likes)
                    replies = toolbar.get('replyCount', '0')
                    if not replies: replies = '0'
                    comments.append({
                        "author": owner.get('displayName'), "author_id": author_id,
                        "author_avatar": owner.get('avatarThumbnailUrl'),
                        "author_url": "https://www.youtube.com/channel/" + author_id if author_id else None,
                        "is_verified": owner.get('isVerified'), "text": properties.get('content', {}).get('content'),
                        "likes": likes, "replies": int(replies.replace(',', '')),
                        "comment_id": properties.get('commentId'),
                        "dislikes": dislikes
                    })

            if not comments:
                break

            def _find_continuation_commands(d, results=None):
                if results is None:
                    results = []

                if isinstance(d, dict):
                    for key, value in d.items():
                        if key == "continuationCommand":
                            results.append(value)
                        else:
                            _find_continuation_commands(value, results)
                elif isinstance(d, list):
                    for item in d:
                        _find_continuation_commands(item, results)

                return results

            try:
                ctoken = _find_continuation_commands(data)[-1].get('token')
            except:
                break
        if not comments:
            _send_warning_message("Couldn't extract comments.", self._ignore_warnings)
        return comments

    @comments.setter
    def comments(self):
        self.comments = None

    def __str__(self):
       return f"<ytget.__main__.Video object with url={self.url}>"

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
    def __init__(self, query: str, get_simple: bool = False, use_threads: bool = True, threads: int = os.cpu_count()//2,
                 max_duration: int = -1, max_results: int = -1, **kwargs):
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
        vids_info = self._search_query()
        self.videos_info = vids_info[:max_results] if max_results > 0 else vids_info
        self.video_urls = list(filter(None, [vid.get('url') for vid in self.videos_info]))
        if not self.video_urls:
            _process_error(er_type="search", data={'query': query, 'is_fatal': True},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        self._get_simple = get_simple
        if self._get_simple:
            return

        self._kwargs = kwargs
        self._download_kwargs = {}
        self._threads = threads
        self._use_threads = use_threads
        self.results = Fetch(iterable=self.video_urls, use_threads=self._use_threads, threads=self._threads, kwargs=self._kwargs)

    def download(self, **download_kwargs):
        """
        Inherits `Video.download()` arguments
        """
        self._download_kwargs.update(download_kwargs)
        self._download_kwargs.setdefault('_show_bar', False)
        if self.results is None:
            _process_error(er_type="download", data={'url': self._query, 'is_fatal': False,
                                            'reason': f'No results found (have you set get_only_urls=True?)'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return

        self._pbar = tqdm(total=len(self.results), unit='videos', desc="Downloading videos")

        if self._use_threads:
            with ThreadPoolExecutor(max_workers=self._threads) as executor:
                executor.map(self._download_vids, self.results, [i for i in range(len(self.results))])
        else:
            for vid in self.results:
                vid.download(**self._download_kwargs)
                self._pbar.update(1)

        self._pbar.close()

    def _download_vids(self, vid, number):
        self._download_kwargs.update({
            "_raw_number": number
        })
        vid.download(**self._download_kwargs)
        self._pbar.update(1)

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
            _process_error(er_type="extract",
                                data={'url': self.url, 'extract_type': 'video info', 'is_fatal': True,
                                      'reason': "Couldn't get json data"},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)

        videos_info = []
        for vid in contents:
            if 'videoRenderer' in vid:
                vid_info = vid.get('videoRenderer')
                video_id = str(vid_info.get('videoId'))
                url = "https://www.youtube.com/watch?v="+video_id
                if url == "https://www.youtube.com/watch?v=None": continue
                thumbnail, title = vid_info.get('thumbnail', {}).get('thumbnails', [{}])[-1], \
                                   vid_info.get('title', {}).get('runs', [{}])[0].get('text')
                fduration, views = vid_info.get('lengthText', {}).get('simpleText', '0:00'), \
                                  re.sub(r'( views|,)', '', vid_info.get('viewCountText', {}).get('simpleText', '-1'))
                duration, fviews = formatted_to_seconds(fduration), _format_views(views)
                if self._max_dur > 0 and duration > self._max_dur:
                    continue
                ch = vid_info.get('longBylineText', {}).get('runs', [{}])[0]
                channel, channel_id = ch.get('text'), \
                                      ch.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                channel_url = "https://www.youtube.com/channel/"+channel_id if channel_id else ''
                videos_info.append({
                    'title': title, 'video_id': video_id, 'url': url, 'duration': duration, 'fduration': fduration,
                    'views': None if views == '-1' else int(views), 'fviews': fviews, 'channel': channel, 'channel_url': channel_url,
                    'channel_id': channel_id
                })
        return videos_info

    def __str__(self):
       return f"<ytget.__main__.Search object with query={self._query}>"

    def __dir__(self):
        """
        Modified dir() to display only common use methods.

        To see the complete dir, use Video().__default_dir__()
        """
        default_dir = super().__dir__()
        return [attribute for attribute in default_dir if not attribute.startswith("_")]

    def __iter__(self):
        return iter(self.videos_info) if self._get_simple else iter(self.results)

    def __len__(self):
        return len(self.videos_info) if self._get_simple else len(self.results)

    def __getitem__(self, index):
        return self.videos_info[index] if self._get_simple else self.results[index]

    def __default_dir__(self):
        return super().__dir__()


class Playlist:
    """
    Get data from a YouTube playlist.

    Attributes
    ----------
    url: str
        A YouTube playlist URL.
        Using a video that's part of a list (has &list= on the name) will also work.
    max_length: int (-1)
        Maximum amount of videos to fetch from the playlist.
    max_duration: int (-1)
        Maximum duration a video can have to fetch it.
    use_threads: bool (True)
        Obtain the information/download the videos using threads (parallel processing)
    threads: int (Half of the available threads)
        Amount of threads to use
    format_duration: bool (True)
        Retrieve the duration of the playlist formatted as HH:MM:SS instead of seconds.
    use_login_playlist: bool (False)
        Login to YouTube only to get the video urls of the playlist (for private playlists).
    kwargs: dict (Default parameters)
        Inherits `Video` kwargs

    Methods
    -------
    download(**download_kwargs)
        Download the videos from the playlist. Inherits `Video.download()` method arguments.
    """
    def __init__(self, url, max_length=-1, max_duration=-1, use_threads=True, threads=os.cpu_count()//2,
                 format_duration=True, use_login_playlist=False, **kwargs):
        kwargs.setdefault('ignore_errors', True)
        kwargs.setdefault('ignore_warnings', True)
        kwargs.setdefault('verbose', False)
        kwargs.setdefault('disable_cache', False)
        self._ignore_errors = kwargs.get("ignore_errors")
        self._ignore_warnings = kwargs.get("ignore_warnings")
        self._verbose = kwargs.get("verbose")
        self._use_threads = use_threads
        self._threads = threads
        self._max_duration = max_duration
        self._max_length = max_length if max_length > 0 else 10000

        self._use_login = use_login_playlist
        self._disable_cache = kwargs.get("disable_cache")
        access_token = None
        if self._use_login:
            access_token = self._get_token()
        self._headers = self._get_headers(access_token=access_token)

        self.url = url
        self.playlist_id = self._extract_playlist_id()
        if not self.playlist_id:
            _process_error(er_type="id", data={'url': self.url, 'is_fatal': True},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        self.playlist_url = "https://www.youtube.com/playlist?list="+self.playlist_id

        self.unavailable_videos = []
        self._playlist_data_info = {}
        self.videos_info = self._extract_videos()
        self.video_urls = [vid.get('url') for vid in self.videos_info]
        self.title = self._playlist_data_info.get('title', {}).get('simpleText')
        self.description = self._playlist_data_info.get('descriptionText', {}).get('simpleText')
        self.length = len(self.video_urls)
        total_length = self._playlist_data_info.get('numVideosText', {}).get('runs', [{}])[0].get('text', '0').replace(',', '')
        self.total_length = int(total_length) if total_length.isnumeric() else 0
        self.views = re.sub(r'( views|,)', '', self._playlist_data_info.get('viewCountText', {}).get('simpleText', '-1'))
        dur = sum(vid.get('duration', 0) for vid in self.videos_info)
        self.duration = format_seconds(dur) if format_duration else dur
        ch = self._playlist_data_info.get('ownerText', {}).get('runs', [{}])[0]
        self.channel = ch.get('text', '').replace('by ', '')
        self.channel_id = ch.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId')
        self.channel_url = "https://www.youtube.com/channel/" + self.channel_id if self.channel_id else ''
        self.banner = self._playlist_data_info.get('playlistHeaderBanner', {}).get('heroPlaylistThumbnailRenderer', {}).get('thumbnail', {}).get('thumbnails', [{}])[-1]

        self._kwargs = kwargs
        self._download_kwargs = {}

    def download(self, _vids=None, **download_kwargs):
        """
        Inherits `Video.download()` arguments
        """
        self._download_kwargs.update(download_kwargs)
        self._download_kwargs.setdefault('_show_bar', False)
        vids = self.videos if not _vids else _vids
        if vids is None:
            _process_error(er_type="download", data={'url': self.url, 'is_fatal': False,
                                            'reason': f'No videos to download'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
            return

        self._pbar = tqdm(total=self.length, unit='videos', desc="Downloading videos")

        if self._use_threads:
            with ThreadPoolExecutor(max_workers=self._threads) as executor:
                executor.map(self._download_vids, vids, [i for i in range(len(vids))])
        else:
            for vid in vids:
                vid.download(**self._download_kwargs)
                self._pbar.update(1)

        self._pbar.close()

    @property
    def videos(self):
        return Fetch(iterable=self.video_urls, use_threads=self._use_threads, threads=self._threads, **self._kwargs)

    @videos.setter
    def videos(self):
        self.videos = []

    def _download_vids(self, vid, number):
        self._download_kwargs.update({
            "_raw_number": number
        })
        vid.download(**self._download_kwargs)
        self._pbar.update(1)

    def _extract_videos(self):
        session = requests.Session()

        req = session.get(self.playlist_url, headers=self._headers)

        if req.status_code != 200:
            _process_error(er_type="extract", data={'url': self.url, 'is_fatal': True,
                                                         'extract_type': 'playlist contents',
                                                         'reason': f'Unsuccessful request - Code <{req.status_code}> | {req.reason}'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find("script", string=re.compile('ytInitialData'))

        json_text = re.search(r'var ytInitialData = ({.*?});', script_tag.string, re.DOTALL).group(1)
        data = json.loads(json_text)

        if data.get('alerts', [{}])[0].get('alertRenderer'):
            _process_error(er_type="extract", data={'url': self.playlist_url, 'is_fatal': True,
                                                          'extract_type': 'playlist contents',
                                                          'reason': 'Private or non-existent playlist'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
        self._playlist_data_info = data.get('header', {}).get('playlistHeaderRenderer', {})
        playlist_contents = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [{}])[0].get('tabRenderer', {}).get('content', {}).get('sectionListRenderer', {}).get('contents', [{}])[0].get('itemSectionRenderer', {}).get('contents', [{}])[0].get('playlistVideoListRenderer', {}).get('contents', [{}])
        ctoken = playlist_contents[-1].get('continuationItemRenderer', {}).get('continuationEndpoint', {}).get('continuationCommand', {}).get('token')

        videos_info = []
        current_result = 1
        for video in playlist_contents:
            if 'playlistVideoRenderer' in video:
                if current_result > self._max_length:
                    return videos_info
                vid_info = video.get('playlistVideoRenderer', {})

                video_id = vid_info.get('videoId')
                title = vid_info.get('title', {}).get('runs', [{}])[0].get('text')
                url = "https://www.youtube.com/watch?v=" + video_id if video_id else None
                fduration = vid_info.get('lengthText', {}).get('simpleText', '0:00')
                duration = formatted_to_seconds(fduration)
                if self._max_duration > 0 and duration > self._max_duration:
                    _send_info_message(f"Skipped `{title}` - {url}: Exceeds set max duration {format_seconds(self._max_duration)}.", verbose=self._verbose)
                    continue
                thumbnail = vid_info.get('thumbnail', {}).get('thumbnails', [{}])[-1].get('url')
                index = int(vid_info.get('index', {}).get('simpleText', -1))
                ch = vid_info.get('shortBylineText', {}).get('runs', [{}])[0]
                channel, channel_id = ch.get('text'), ch.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                channel_url = "https://www.youtube.com/channel/" + channel_id if channel_id else ''
                views_match = re.search(r'(\d{1,3}(?:,\d{3})*) views', vid_info.get('title', {}).get('accessibility', {}).get('accessibilityData', {}).get('label'))
                views = views_match.group(1).replace(',', '') if views_match else '-1'
                fviews = _format_views(views)

                vid_dict = {
                    'title': title, 'video_id': video_id, 'url': url, 'duration': duration, 'fduration': fduration,
                    'views': None if views == '-1' else int(views), 'fviews': fviews, 'channel': channel,
                    'channel_url': channel_url, 'channel_id': channel_id, 'index': index, 'thumbnail': thumbnail
                }

                if not vid_info.get('isPlayable', True):
                    self.unavailable_videos.append(vid_dict)
                    _send_info_message(f"Skipped `{title}` - {url}: Video Unavailable.", verbose=self._verbose)
                    continue
                videos_info.append(vid_dict)
                current_result += 1

        while ctoken:
            base_url = "https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
            payload = CLIENT_INFO['web']['payload'].copy()
            payload.update({
                'continuation': ctoken
            })
            response = session.post(base_url, headers=CLIENT_INFO['web']['headers'], json=payload)
            if response.status_code != 200:
                _process_error(er_type="extract", data={'url': self.url, 'is_fatal': False,
                                                             'extract_type': 'playlist contents',
                                                             'reason': f'Unsuccessful request - Code <{response.status_code}> | {response.reason}'},
                           ignore_errors=self._ignore_errors, ignore_warnings=self._ignore_warnings)
                break
            data = response.json()

            next_video_list = data.get('onResponseReceivedActions', [{}])[0].get('appendContinuationItemsAction',
                                                                                 {}).get('continuationItems', [{}])
            ctoken = next_video_list[-1].get('continuationItemRenderer', {}).get('continuationEndpoint', {}).get(
                'continuationCommand', {}).get('token')

            for video in next_video_list:
                if 'playlistVideoRenderer' in video:
                    if current_result > self._max_length:
                        return videos_info
                    vid_info = video.get('playlistVideoRenderer', {})

                    video_id = vid_info.get('videoId')
                    title = vid_info.get('title', {}).get('runs', [{}])[0].get('text')
                    url = "https://www.youtube.com/watch?v=" + video_id if video_id else None

                    fduration = vid_info.get('lengthText', {}).get('simpleText', '0:00')
                    duration = formatted_to_seconds(fduration)
                    if self._max_duration > 0 and duration > self._max_duration:
                        _send_info_message(f"Skipped `{title}` - {url}: Exceeds set max duration {format_seconds(self._max_duration)}.", verbose=self._verbose)
                        continue
                    thumbnail = vid_info.get('thumbnail', {}).get('thumbnails', [{}])[-1].get('url')
                    index = int(vid_info.get('index', {}).get('simpleText', -1))
                    ch = vid_info.get('shortBylineText', {}).get('runs', [{}])[0]
                    channel, channel_id = ch.get('text'), ch.get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', '')
                    channel_url = "https://www.youtube.com/channel/" + channel_id if channel_id else ''
                    views_match = re.search(r'(\d{1,3}(?:,\d{3})*) views',vid_info.get('title', {}).get('accessibility', {}).get('accessibilityData',{}).get('label'))
                    views = views_match.group(1).replace(',', '') if views_match else '-1'
                    fviews = _format_views(views)

                    vid_dict = {
                        'title': title, 'video_id': video_id, 'url': url, 'duration': duration, 'fduration': fduration,
                        'views': None if views == '-1' else int(views), 'fviews': fviews, 'channel': channel,
                        'channel_url': channel_url, 'channel_id': channel_id, 'index': index, 'thumbnail': thumbnail
                    }
                    if not vid_info.get('isPlayable', True):
                        self.unavailable_videos.append(vid_dict)
                        _send_info_message(f"Skipped `{title}` - {url}: Video Unavailable.", verbose=self._verbose)
                        continue
                    videos_info.append(vid_dict)
                    current_result += 1

        return videos_info

    def _extract_playlist_id(self):
        yt_playlist_match = re.search(r"(?:https?:\/\/(?:www\.|m\.)?youtube\.com\/.*[?&]list=|https?:\/\/youtu\.be\/)([a-zA-Z0-9_-]*)", self.url)
        if yt_playlist_match:
            return yt_playlist_match.group(1)

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
        _send_info_message("Logging in...", ignore_verbose=True, verbose=self._verbose)
        _send_info_message(f"Open {response_data.get('verification_url')} and use the code {response_data.get('user_code')}", ignore_verbose=True, verbose=self._verbose)
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

    def __str__(self):
        return f"`Playlist` object at {hex(id(self))}, title: {self.title}, url: {self.playlist_url}, id: {self.playlist_id}, videos: {self.length}"

    def __repr__(self):
        return f"`Playlist` object at {hex(id(self))}, title: {self.title}, url: {self.playlist_url}, id: {self.playlist_id}, videos: {self.length}"

    def __dir__(self):
        """
        Modified dir() to display only common use methods.

        To see the complete dir, use Video().__default_dir__()
        """
        default_dir = super().__dir__()
        return [attribute for attribute in default_dir if not attribute.startswith("_")]

    def __iter__(self):
        return iter(self.videos_info)

    def __len__(self):
        return self.length

    def __add__(self, other):
        if not isinstance(other, Playlist):
            if isinstance(other, list) or isinstance(other, tuple):
                return self.videos_info + other
            raise TypeError(f"Unsupported operand type(s) for +: 'Playlist' and '{type(other).__name__}'")
        return self.videos_info + other.videos_info

    def __radd__(self, other):
        if not isinstance(other, Playlist):
            if isinstance(other, list) or isinstance(other, tuple):
                return other + self.videos_info
            raise TypeError(f"Unsupported operand type(s) for +: 'Playlist' and '{type(other).__name__}'")
        return other.videos_info + self.videos_info

    def __getitem__(self, index):
        return self.videos_info[index]

    def __setitem__(self, index, value):
        self.videos_info[index] = value

    def __contains__(self, item):
        if isinstance(item, dict):
            return any(item == video for video in self.videos_info) or any(item.get('url') == url for url in self.video_urls)
        return any(item == video['title'] or item == video['url'] or item == video['video_id'] for video in self.videos_info) or any(item == url for url in self.video_urls)

    def append(self, item):
        self.videos_info.append(item)
        self.video_urls.append(item.get('url') if isinstance(item, dict) else item)

    def extend(self, item):
        self.videos_info.extend(item)
        self.video_urls.extend(item.get('url') if isinstance(item, dict) else item)

    def remove(self, item):
        self.videos_info = [video for video in self.videos_info if item not in {video.get('title'), video.get('url'), video.get('video_id')}]
        self.video_urls = [video.get('url') for video in self.videos_info]
        self.length = len(self.video_urls)

    def pop(self, index=-1):
        return self.videos_info.pop(index)

    def clear(self):
        self.videos_info.clear()

    def sort(self, key=None, reverse=False):
        self.videos_info.sort(key=key, reverse=reverse)

    def reverse(self):
        self.videos_info.reverse()

    def __default_dir__(self):
        return super().__dir__()


class Fetch:
    """
    Get information of videos from a list of urls or dicts with video info.
    """
    def __new__(cls, iterable: Union[Iterable[str | Dict]], use_threads: bool = True, threads: int = os.cpu_count()//2, **kwargs) -> List[Video]:
        """
        Get information of videos from a list of urls or dicts with video info.

        :param iterable: List of video URLs or dicts with video info (they need to have a "url" key)
        :param use_threads: Use parallel processing for faster fetching
        :param threads: Amount of threads to use
        :param kwargs: Inherited from `Video` class kwargs
        """
        instance = super().__new__(cls)
        vid_urls = [item.get('url') if isinstance(item, dict) else item for item in iterable]
        kwargs.setdefault("ignore_warnings", True)

        if use_threads:
            def _fetch_info(url):
                return Video(url, **kwargs)

            with ThreadPoolExecutor(max_workers=threads) as executor:
                instance.videos = list(executor.map(_fetch_info, vid_urls))
        else:
            instance.videos = []
            for url in vid_urls:
                instance.videos.append(Video(url, **kwargs))

        return instance.videos
