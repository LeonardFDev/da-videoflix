"""create thumbnail task"""

import subprocess
import random

from pathlib import Path
from video_app.models import Video


def create_thumbnail(move_video_file, video_id):
    """Initialization of thumbnail creation."""

    result = find_video_runtime(move_video_file)
    duration = float(result.stdout.strip())
    random_timestamp = random.uniform(duration * 0.2, duration * 0.8)

    thumbnail_path = Path(move_video_file).parent / "thumbnail.jpg"
    create_video_thumbnail(move_video_file, random_timestamp, thumbnail_path)

    Video.objects.filter(id=video_id).update(thumbnail_url=f"video/{video_id}/thumbnail.jpg")

def find_video_runtime(move_video_file):
    """Returns information of the video, including the required length of the video"""

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
    """Executes the command that creates a thumbnail at a random location in the video"""

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