"""Video conversion task"""

import subprocess

from pathlib import Path
from video_app.models import Video
from .create_thumbnail import create_thumbnail


def convert_and_create_hls(input_video, video_id):
    """Initialization of video conversion."""

    move_video_file = move_video_file_to_id_folder(input_video, video_id)
    base_dir = Path(move_video_file).parent
    base_dir.mkdir(parents=True, exist_ok=True)

    resolution_conversion_loop(base_dir, move_video_file)
    create_thumbnail(move_video_file, video_id)

    Video.objects.filter(id=video_id, is_ready=False).update(is_ready=True)


def move_video_file_to_id_folder(input_video, video_id):
    """Move the input video to the id folder"""

    source = Path(input_video)

    destination = Path(input_video).parent / str(video_id) / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    source.rename(destination)

    Video.objects.filter(id=video_id).update(video_file=destination)

    return str(destination)


def resolution_conversion_loop(base_dir, move_video_file):
    """Converts all resolutions"""

    resolutions = get_reresolutions()

    for name, height in resolutions.items():
        output_dir = Path(base_dir) / name
        output_dir.mkdir(parents=True, exist_ok=True)
    
        playlist = Path(output_dir) / "index.m3u8"
        segment_pattern = Path(output_dir) / "segment_%03d.ts"
    
        command = get_command(move_video_file, height, segment_pattern, playlist)
    
        subprocess.run(command, check=True)


def get_reresolutions():
    """Return the resolutions"""

    return {
        "1080p": 1080,
        "720p": 720, 
        "480p": 480,
    }


def get_command(move_video_file, height, segment_pattern, playlist):
    """Return the ffmpeg/hls command"""
    
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