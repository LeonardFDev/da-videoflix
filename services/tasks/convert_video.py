import subprocess
import random

from pathlib import Path
from video_app.models import Video


def convert_and_create_hls(input_video, video_id):
    move_video_file = move_video_file_to_id_folder(input_video, video_id)
    base_dir = Path(move_video_file).parent
    base_dir.mkdir(parents=True, exist_ok=True)

    resolutions = get_reresolutions()

    resolution_conversion_loop(resolutions, base_dir, move_video_file)
    create_thumbnail(move_video_file, video_id)

    Video.objects.filter(id=video_id, is_ready=False).update(is_ready=True)


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


def create_thumbnail(move_video_file, video_id):
    result = find_video_runtime(move_video_file)
    duration = float(result.stdout.strip())
    random_timestamp = random.uniform(duration * 0.2, duration * 0.8)

    thumbnail_path = Path(move_video_file).parent / "thumbnail.jpg"
    create_video_thumbnail(move_video_file, random_timestamp, thumbnail_path)

    Video.objects.filter(id=video_id).update(thumbnail_url=f"video/{video_id}/thumbnail.jpg")

def find_video_runtime(move_video_file):
    return subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            move_video_file,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

def create_video_thumbnail(move_video_file, random_timestamp, thumbnail_path):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", move_video_file,
            "-ss", str(random_timestamp),
            "-frames:v", "1",
            "-vf", "scale=640:-1",
            str(thumbnail_path),
        ],
        check=True,
    )