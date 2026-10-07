import os
import subprocess

INPUT_FOLDER = "raw_footage"
OUTPUT_FOLDER = "static"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.exists(INPUT_FOLDER):
    print(f"Error: Input folder '{INPUT_FOLDER}' not found.")
    exit()

video_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith((".mp4", ".mov", ".mkv"))]

if not video_files:
    print(f"No video files found in '{INPUT_FOLDER}'.")
    exit()

print(f"Found {len(video_files)} video(s) to compress (HIGH QUALITY).\n")

for filename in video_files:
    input_path = os.path.join(INPUT_FOLDER, filename)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_compressed.mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # HIGH QUALITY settings:
    # - scale=3840:1920 (4K 360°, good balance)
    #   OR scale=-2:1920 (if you want to keep original aspect ratio, height=1920)
    # - crf 18 (visually lossless for most content)
    # - preset medium (better compression than 'fast')
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "scale=3840:1920",   # 4K 360° resolution
        "-c:v", "libx264",
        "-crf", "18",               # Higher quality (lower = better)
        "-preset", "medium",        # Better quality/size trade-off
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        "-y",
        output_path
    ]

    print(f"Compressing: {filename} -> {output_filename} (4K, CRF 18)")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Success: {output_path}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compressing {filename}: {e}\n")

print("All done!")