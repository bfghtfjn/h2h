import os
import secrets
from flask import Flask, request, jsonify, send_from_directory
from uuid import uuid4
from pathlib import Path
import yt_dlp
from constants import *

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube to MP3 API is running!"

@app.route("/convert", methods=["GET"])
def convert_audio():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify(error="Missing 'url' parameter."), BAD_REQUEST

    # Ensure the downloads directory exists
    Path(ABS_DOWNLOADS_PATH).mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4()}.mp3"
    output_path = Path(ABS_DOWNLOADS_PATH) / filename

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path),
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        return jsonify(error="Download failed", detail=str(e)), INTERNAL_SERVER_ERROR

    return jsonify(link=f"/download/{filename}")

@app.route("/download/<filename>")
def download_audio(filename):
    file_path = Path(ABS_DOWNLOADS_PATH) / filename
    if not file_path.exists():
        return jsonify(error="File not found"), NOT_FOUND

    return send_from_directory(ABS_DOWNLOADS_PATH, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)