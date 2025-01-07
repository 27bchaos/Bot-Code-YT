import os
import time
import subprocess
import yt_dlp

# Replace this with your own stream URL and Stream Key
STREAM_URL = "rtmp://a.rtmp.youtube.com/live2"  # YouTube RTMP server
STREAM_KEY = "YOUR_STREAM_KEY"  # Replace with your YouTube stream key

# The YouTube video URL you want to stream
VIDEO_URL = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'  # Replace with your actual video URL

def stream_video(video_url):
    """Use yt-dlp to fetch the video stream and send it to YouTube Live using FFmpeg."""
    # Use yt-dlp to get the best video and audio streams
    ydl_opts = {
        'format': 'bestaudio/best',  # Get the best audio and video streams
        'outtmpl': '-',  # Output to stdout (pipe to FFmpeg)
        'quiet': True,  # Disable yt-dlp logs
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        print(f"Streaming video: {info_dict.get('title')}")

        # Set up FFmpeg to stream the content to YouTube Live
        ffmpeg_command = [
            'ffmpeg',
            '-re',  # Read input at native frame rate
            '-i', '-',  # Input from the yt-dlp pipe (stdout)
            '-c:v', 'libx264',  # Video codec (H.264)
            '-c:a', 'aac',  # Audio codec (AAC)
            '-b:a', '192k',  # Set audio bitrate
            '-preset', 'veryfast',  # Encoding preset
            '-f', 'flv',  # FLV format (required by RTMP)
            f'{STREAM_URL}/{STREAM_KEY}'  # Your stream URL with key
        ]

        # Pipe the yt-dlp output to FFmpeg's input
        process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
        try:
            ydl.download([video_url])  # Start streaming the video
            while True:
                time.sleep(60)  # Stream continuously
        except KeyboardInterrupt:
            print("Live stream ended.")
        finally:
            process.terminate()

if __name__ == "__main__":
    # Start the live stream
    stream_video(VIDEO_URL)
