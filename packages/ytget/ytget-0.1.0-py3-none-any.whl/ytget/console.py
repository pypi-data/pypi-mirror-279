import argparse
import os
import json

from .__main__ import Video, Search
from .exceptions import SearchError, DownloadError, ForbiddenError, ExtractError
from .out_colors import (_yellow, _green, _dim_cyan, _red)


def cmd_parser():
    parser = argparse.ArgumentParser(
        description='Easily get data and download youtube videos, focused on speed and simplicity.',
        epilog='Note: The --print argument must be placed after the query.'
    )

    general_group = parser.add_argument_group('general')
    json_group = parser.add_argument_group('json')
    search_group = parser.add_argument_group('search params')
    video_group = parser.add_argument_group('video params')
    download_group = parser.add_argument_group('download')

    # general
    general_group.add_argument('query', type=str, help='URL or query to search')
    general_group.add_argument('--print', type=str, nargs='+', metavar='INFO', help='Show the specified info on screen')
    general_group.add_argument('-y', action='store_true', help='Automatically confirm Y on prompt', default=False)
    general_group.add_argument('-s', '--skip-download', action='store_true', help='Don\'t download the stream', default=False)
    general_group.add_argument('--ignore-errors', action='store_true', help='Proceed anyways in case of non-fatal error', default=False)
    general_group.add_argument('--ignore-warnings', action='store_true', help='Ignore printing warning messages', default=False)
    general_group.add_argument('-v', '--verbose', action='store_true', help='Show info messages', default=False)

    # json
    json_group.add_argument('--write-to-json', action='store_true', help='Write the info specified on "--print" to a json', default=False)
    json_group.add_argument('--json-path', type=str, metavar='PATH', help='Output path for json files', default=".")

    # search related
    search_group.add_argument('--search', action='store_true', help='Shows results for the query instead of downloading', default=False)
    search_group.add_argument('--disable-threads', action='store_true', help='Disable parallel processing on batch processes', default=False)
    search_group.add_argument('--threads', type=int, help='Amount of threads to use on batch processes', default=os.cpu_count()//2)
    search_group.add_argument('--max-duration', type=int, metavar='SECONDS', help='Max duration a video can have when searching to fetch it', default=-1)

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

    # download related
    download_group.add_argument('-p', '--path', type=str, help='Output path for downloads', default=".")
    download_group.add_argument('--quality', type=str, help='Quality to download (best, high, med, low, lowest)', default="best")
    download_group.add_argument('--only-video', action='store_true', help='Get stream with only video', default=False)
    download_group.add_argument('--only-audio', action='store_true', help='Get stream with only audio, overrides --only-video', default=False)
    download_group.add_argument('--target-fps', type=int, metavar='FPS', help='Target fps for the video stream, gets closest result', default=60)
    download_group.add_argument('--target-itag', type=int, metavar='ITAG', help='Target itag for the stream', default=-1)
    download_group.add_argument('--audio-format', type=str, metavar='FORMAT', help='Preferred audio format to save into', default="mp3")
    download_group.add_argument('--video-format', type=str, metavar='FORMAT', help='Preferred video format to save into', default="mp4")
    download_group.add_argument('--chunk-size', type=int, help='Stream download chunk size', default=1024*1024)
    download_group.add_argument('--force-ffmpeg', action='store_true', help='Force conversion from bytes with ffmpeg', default=False)


    args = parser.parse_args()

    print_dict = {
        "title": args.search, "url": args.search, "video_id": False,
        "channel": False, "channel_id": False, "channel_picture": False, "channel_url": False, "chapters": False,
        "description": False, "duration": False, "is_live": False, "keywords": False, "publish_date": False,
        "stream_url": False, "subtitles": False, "thumbnail": False, "upload_date": False, "views": False
    }

    argument_dict = {
        "get_duration_formatted": not args.no_format_duration,
        "get_channel_picture": not args.no_channel_picture,
        "get_views_formatted": args.format_views,
        "thumbnail_quality": args.thumbnail_quality,
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
        'chunk_size': args.chunk_size, 'force_ffmpeg': args.force_ffmpeg
    }

    outputs = args.print
    if outputs:
        failed_prints = []
        for arg in outputs:
            arg = arg.lower()
            if arg == 'all':
                for key in print_dict:
                    print_dict[key] = True
                break
            if arg not in print_dict:
                failed_prints.append(arg)
                continue
            print_dict[arg] = True
        if failed_prints:
            print(_yellow("[WARNING]: Invalid print arguments: "+", ".join(failed_prints)))

    if args.search:
        search_obj = Search(args.query, get_simple=False, use_threads=not args.disable_threads,
                         threads=args.threads, max_duration=args.max_duration, **argument_dict)
        results = search_obj.results
        for video in results:
            for output in print_dict:
                if hasattr(video, output) and print_dict[output]:
                    print(_dim_cyan(output + ":"), getattr(video, output), end=" | ")
            print("")

        if not args.skip_download:
            if args.y:
                search_obj.download(**download_kwargs)
            else:
                confirmation = str(input(_red("Would you like to download the results? (Y/N) ")))[0].lower()
                if confirmation == 'y':
                    search_obj.download(**download_kwargs)
    else:
        vid = Video(args.query, **argument_dict)
        if not args.skip_download:
            vid.download(**download_kwargs)
        else:
            print(_green(f"[SUCCESS]: Fetched info for `{vid.url}`: `{vid.title}`."))
        for output in print_dict:
            if hasattr(vid, output) and print_dict[output]:
                print(_dim_cyan(output+":"), getattr(vid, output))

    if args.write_to_json:
        if not print_dict:
            print(_yellow(f"[WARNING]: Couldn't write to json - No information to write, use `--print` to get the info."))
        json_data = {}
        if args.search:
            for i, vid in enumerate(results):
                title = vid.title if vid.title else f"none_{i}"
                json_data[title] = {}
                for output in print_dict:
                    if hasattr(video, output) and print_dict[output]:
                        json_data[title].update({f'{output}': getattr(vid, output)})
        else:
            for output in print_dict:
                if hasattr(vid, output) and print_dict[output]:
                    json_data.update({f'{output}': getattr(vid, output)})
        with open(os.path.abspath(os.path.join(args.json_path, "video_data.json")), "w") as f:
            json.dump(json_data, f)


if __name__ == '__main__':
    cmd_parser()
