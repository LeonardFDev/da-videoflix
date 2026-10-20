import subprocess


def convert1080p(source):
    new_file_name = source.replace("_original.mp4", "") + "_1080p.mp4"

    # cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(source),
        "-vf", "scale=-2:1080",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(new_file_name),
    ]
    subprocess.run(cmd, capture_output=True)


def convert720p(source):
    new_file_name = source.replace("_original.mp4", "") + "_720p.mp4"

    # cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(source),
        "-vf", "scale=-2:720",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(new_file_name),
    ]
    subprocess.run(cmd, capture_output=True)


def convert480p(source):
    new_file_name = source.replace("_original.mp4", "") + "_480p.mp4"

    # cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(source),
        "-vf", "scale=-2:480",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        str(new_file_name),
    ]
    subprocess.run(cmd, capture_output=True)