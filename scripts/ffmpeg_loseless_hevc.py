## Description: Loseless x265 encoding using FFmpeg

import subprocess

def encode_with_ffmpeg():
    # If 'ffmpeg' is not on your system PATH, replace 'ffmpeg' 
    # with the full path to your ffmpeg.exe, for example:
    # ffmpeg_binary = "C:/path/to/ffmpeg.exe"
    ffmpeg_binary = "C:\ffmpeg\ffmpeg.exe"
    
    # Build the command as a list of arguments
    command = [
        ffmpeg_binary,
        "-i", "video.avi",           # The input video file
        "-c:v", "libx265",           # Use libx265 (H.265/HEVC) for video encoding
        "-crf", "0",                 # CRF = 0 (together with lossless=1 ensures lossless encoding)
        "-preset", "veryslow",       # Use the 'veryslow' preset for maximally optimising compression (though slower)
        "-x265-params", "lossless=1",# Enforce x265 to produce a lossless encode
        "-c:a", "copy",              # Copy the existing audio tracks without re-encoding
        "-c:s", "copy",              # Copy the existing subtitle streams without re-encoding
        "-map_chapters", "0",        # Preserve chapter markers from the input file
        "C:\output.mkv"                 # The output file name
    ]
    
    # Run ffmpeg with the above arguments, capturing output for debugging
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print ffmpeg's console output and any errors
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

if __name__ == "__main__":
    encode_with_ffmpeg()
