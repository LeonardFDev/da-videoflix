import subprocess

from pathlib import Path
from video_app.models import Video


def convert_and_create_hls(input_video, video_id):
    move_video_file = move_video_file_to_id_folder(input_video, video_id)
    base_dir = Path(move_video_file).parent
    base_dir.mkdir(parents=True, exist_ok=True)

    resolutions = get_reresolutions()

    resolution_conversion_loop(resolutions, base_dir, move_video_file)


def move_video_file_to_id_folder(input_video, video_id):
    source = Path(input_video)

    destination = Path(input_video).parent / str(video_id) / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    source.rename(destination)

    Video.objects.filter(id=video_id).update(video_file=destination)

    return str(destination)


def get_reresolutions():
    return {
        "1080p": {"height": 1080, "bandwidth": 5000000},
        "720p": {"height": 720, "bandwidth": 2800000},
        "480p": {"height": 480, "bandwidth": 1400000},
    }


def resolution_conversion_loop(resolutions, base_dir, move_video_file):
    for name, config in resolutions.items():
        height = config["height"]
    
        output_dir = Path(base_dir) / name
        output_dir.mkdir(parents=True, exist_ok=True)
    
        playlist = Path(output_dir) / "index.m3u8"
        segment_pattern = Path(output_dir) / "segment_%03d.ts"
    
        command = get_command(move_video_file, height, segment_pattern, playlist)
    
        subprocess.run(command, check=True)


def get_command(move_video_file, height, segment_pattern, playlist):
    return [
        "ffmpeg",
        "-y",
        "-i", move_video_file,
        "-vf", f"scale=-2:{height}",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-hls_segment_filename", segment_pattern,
        "-f", "hls",
        playlist,
    ]