import imageio_ffmpeg
import subprocess
import os
import re

ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

def get_duration(path):
    cmd = [ffmpeg_path, "-i", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        h, m, s = match.groups()
        total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
        return f"{total_seconds:.1f}"
    return "unknown"

pairs = [
    ("raw_footage/intro.mp4", "static/intro_compressed.mp4"),
    ("raw_footage/port_city.mp4", "static/port_city_compressed.mp4"),
    ("raw_footage/independence_square.mp4", "static/independence_square_compressed.mp4"),
    ("raw_footage/planetarium.mp4", "static/planetarium_compressed.mp4"),
    ("raw_footage/viharamahadevi_park.mp4", "static/viharamahadevi_park_compressed.mp4"),
]

for original, compressed in pairs:
    if os.path.exists(original) and os.path.exists(compressed):
        orig_dur = get_duration(original)
        comp_dur = get_duration(compressed)
        print(f"{os.path.basename(original)}: original={orig_dur}s, compressed={comp_dur}s")
    else:
        print(f"Missing file(s) for: {original} / {compressed}")