import argparse
import os
import json

from .__main__ import Video, Search, Playlist
from .out_colors import (_dim_cyan, _red)
from .utils import (_send_warning_message, _send_info_message, _send_success_message)


def cmd_parser():
    parser = argparse.ArgumentParser(
        description='Easily get data and download youtube videos, focused on speed and simplicity.',
        epilog='Notes: The --print argument might need to be placed after the query. Some queries might need quotes ("") to be taken correctly.'
    )

    general_group = parser.add_argument_group('general')
    json_group = parser.add_argument_group('json')
    search_group = parser.add_argument_group('search params')
    video_group = parser.add_argument_group('video params')
    download_group = parser.add_argument_group('downloads')
    playlist_group = parser.add_argument_group('playlists', 'inherits video+download parameters')
    config_group = parser.add_argument_group('configuration')

    parser.add_argument('query', type=str, help='URL or query to search')

    # general
    general_group.add_argument('--print', type=str, nargs='+', metavar='INFO', help='Show the specified info on screen')
    general_group.add_argument('-y', action='store_true', help='Automatically confirm on prompt', default=False)
    general_group.add_argument('-s', '--skip-download', action='store_true', help='Don\'t download the stream', default=False)
    general_group.add_argument('-v', '--verbose', action='store_true', help='Show info messages', default=False)

    # json
    json_group.add_argument('--write-to-json', action='store_true', help='Write the info specified on "--print" to a json', default=False)
    json_group.add_argument('--json-path', type=str, metavar='PATH', help='Output path for json files', default=".")

    # search related
    search_group.add_argument('--search', action='store_true', help='Shows results for the query instead of downloading', default=False)
    search_group.add_argument('--max-results', type=int, help='Max amount of videos to fetch from the result', default=-1)
    search_group.add_argument('--max-duration', type=int, metavar='SECONDS', help='Max duration a video can have when searching or in a playlist to fetch it', default=-1)

    # video class related
    video_group.add_argument('--use-login', action='store_true', help='Login into youtube', default=False)
    video_group.add_argument('--disable-cache', action='store_true', help='Disables saving cache for oauth, requires logging in again', default=False)
    video_group.add_argument('--no-retry', action='store_true', help='Disables retrying in case of error', default=False)
    video_group.add_argument('--client', type=str, help='Client to use (android, android_music, android_creator, web)', default="android_music")
    video_group.add_argument('--no-format-duration', action='store_true', help='Disable formatting the duration as HH:MM:SS, returns in seconds instead', default=False)
    video_group.add_argument('--format-views', action='store_true', help='Format the views like this example: "1951483" to "1 951 483"', default=False)
    video_group.add_argument('--no-channel-picture', action='store_true', help='Disables fetching the channel picture', default=False)
    video_group.add_argument('--thumbnail-quality', type=str, help='Quality of the thumbnail to fetch (best, high, med, low)', default="best")
    video_group.add_argument('--date-format', type=str, metavar='FORMAT', help='Format of the publish/upload dates (eu, us, sql, unix, iso)', default="eu")
    video_group.add_argument('--comments', action='store_true', help='Get video comments when using --print all.', default=False)
    video_group.add_argument('--max-comments', type=int, help='Max comments to fetch', default=60)

    # download related
    download_group.add_argument('-p', '--path', type=str, help='Output path for downloads', default=".")
    download_group.add_argument('--quality', type=str, help='Quality to download (best, high, med, low, lowest)', default="best")
    download_group.add_argument('--keep', action='store_true', help='Keep separate streams (in case there are any)', default=False)
    download_group.add_argument('--only-video', action='store_true', help='Get stream with only video', default=False)
    download_group.add_argument('--only-audio', action='store_true', help='Get stream with only audio, overrides --only-video', default=False)
    download_group.add_argument('--target-fps', type=int, metavar='FPS', help='Target fps for the video stream, gets closest result', default=60)
    download_group.add_argument('--target-itag', type=int, metavar='ITAG', help='Target itag for the stream', default=-1)
    download_group.add_argument('--audio-format', type=str, metavar='FORMAT', help='Preferred audio format to save into', default="mp3")
    download_group.add_argument('--video-format', type=str, metavar='FORMAT', help='Preferred video format to save into', default="mp4")
    download_group.add_argument('--chunk-size', type=int, help='Stream download chunk size', default=1024*1024)
    download_group.add_argument('--force-ffmpeg', action='store_true', help='Force conversion from bytes with ffmpeg, use in case of broken file', default=False)

    # playlist related
    playlist_group.add_argument('--force-playlist', action='store_true', help='Force using the given query as a playlist url', default=False)
    playlist_group.add_argument('--max-length', type=int, help='Maximum videos to fetch from the playlist', default=-1)
    playlist_group.add_argument('--no-format-total-duration', action='store_true', help='Disable formatting the total duration of the playlist as HH:MM:SS, returns in seconds instead', default=False)
    playlist_group.add_argument('--use-login-playlist', action='store_true', help='Login into youtube only to access the playlist', default=False)

    # config
    config_group.add_argument('--ignore-errors', action='store_true', help='Proceed anyways in case of non-fatal error', default=False)
    config_group.add_argument('--ignore-warnings', action='store_true', help='Ignore printing warning messages', default=False)
    config_group.add_argument('--disable-threads', action='store_true', help='Disable parallel processing on batch processes', default=False)
    config_group.add_argument('--threads', type=int, help='Amount of threads to use on batch processes', default=os.cpu_count() // 2)

    # extra
    # --fetch-from-file (usa Fetch para agarrar datos de un .txt o .json, automaticamente detectar ciertos modos: separados por \n, ;, etc)
    # hacer que Fetch pueda usar sin threads

    args = parser.parse_args()

    print_dict = {
        "title": args.search, "url": args.search, "video_id": False,
        "channel": False, "channel_id": False, "channel_picture": False, "channel_url": False, "chapters": False,
        "description": False, "duration": False, "is_live": False, "keywords": False, "publish_date": False,
        "stream_url": False, "subtitles": False, "thumbnail": False, "upload_date": False, "views": False,
        "comments": False
    }

    argument_dict = {
        "get_duration_formatted": not args.no_format_duration,
        "get_channel_picture": not args.no_channel_picture,
        "thumbnail_quality": args.thumbnail_quality,
        "max_comments": args.max_comments,
        "get_views_formatted": args.format_views,
        "date_format": args.date_format,
        "use_login": args.use_login,
        "disable_cache": args.disable_cache,
        "ignore_errors": args.ignore_errors,
        "ignore_warnings": args.ignore_warnings,
        "verbose": args.verbose,
        "no_retry": args.no_retry,
        "client": args.client
    }
    download_kwargs = {
        'path': args.path, 'quality': args.quality, 'only_video': all([args.only_video, not args.only_audio]),
        'only_audio': args.only_audio, 'target_fps': args.target_fps, 'target_itag': args.target_itag,
        'preferred_audio_format': args.audio_format, 'preferred_video_format': args.video_format,
        'chunk_size': args.chunk_size, 'force_ffmpeg': args.force_ffmpeg, 'keep': args.keep
    }

    outputs = args.print
    if outputs:
        failed_prints = []
        for arg in outputs:
            arg = arg.lower()
            if arg == 'all':
                for key in print_dict:
                    if key == "comments" and not args.comments: continue
                    print_dict[key] = True
                break
            if arg not in print_dict:
                failed_prints.append(arg)
                continue
            print_dict[arg] = True
        if failed_prints:
            _send_warning_message("Invalid print arguments: "+", ".join(failed_prints), False)

    if args.search:
        search_obj = Search(args.query, get_simple=False, use_threads=not args.disable_threads,  threads=args.threads,
                            max_duration=args.max_duration, max_results=args.max_results, **argument_dict)
        results = search_obj.results
        for video in results:
            new_line = False
            for output in print_dict:
                if output in dir(video) and print_dict[output]:
                    print(_dim_cyan(output + ":"), getattr(video, output), end=" | ")
                    new_line = True
            if new_line: print("")

        if not args.skip_download:
            if args.y:
                search_obj.download(**download_kwargs)
            else:
                confirmation = str(input(_red("Would you like to download the results? (Y/N) ")))[0].lower()
                if confirmation == 'y':
                    search_obj.download(**download_kwargs)
    else:
        is_playlist = False
        def _playlist_fetch():
            playlist = Playlist(args.query, max_length=args.max_length, max_duration=args.max_duration,
                                use_threads=not args.disable_threads, threads=args.threads,
                                format_duration=not args.no_format_total_duration,
                                use_login_playlist=args.use_login_playlist, **argument_dict)
            videos = playlist.videos
            if not args.skip_download:
                playlist.download(_vids=videos, **download_kwargs)
            else:
                _send_success_message(f"Fetched info for playlist `{playlist.playlist_url}`: `{playlist.title}`.", True)
            for vid in videos:
                new_line = False
                for output in print_dict:
                    if output in dir(vid) and print_dict[output]:
                        print(_dim_cyan(output + ":"), getattr(vid, output), end=" | ")
                        new_line = True
                if new_line: print("")

            return videos

        if args.force_playlist:
            vids = _playlist_fetch()
            is_playlist = True
        else:
            try:
                vid = Video(args.query, **argument_dict)
                if not args.skip_download:
                    vid.download(**download_kwargs)
                else:
                    _send_success_message(f"Fetched info for `{vid.url}`: `{vid.title}`.", True)
                for output in print_dict:
                    if output in dir(vid) and print_dict[output]:
                        print(_dim_cyan(output+":"), getattr(vid, output))
            except:
                is_playlist = True
                vids = _playlist_fetch()

    if args.write_to_json:
        if not print_dict:
            _send_warning_message(f"Couldn't write to json - No information to write, use `--print` to get the info.", False)
        json_data = {}
        if args.search:
            for i, vid in enumerate(results):
                title = vid.title if vid.title else f"none_{i}"
                json_data[title] = {}
                for output in print_dict:
                    if output in dir(vid) and print_dict[output]:
                        json_data[title].update({f'{output}': getattr(vid, output)})
        elif is_playlist:
            for i, vid in enumerate(vids):
                title = vid.title if vid.title else f"none_{i}"
                json_data[title] = {}
                for output in print_dict:
                    if output in dir(vid) and print_dict[output]:
                        json_data[title].update({f'{output}': getattr(vid, output)})
        else:
            for output in print_dict:
                if output in dir(vid) and print_dict[output]:
                    json_data.update({f'{output}': getattr(vid, output)})
        with open(os.path.abspath(os.path.join(args.json_path, "video_data.json")), "w") as f:
            json.dump(json_data, f)


if __name__ == '__main__':
    cmd_parser()
