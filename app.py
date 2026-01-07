from flask import Flask, send_file
import yt_dlp
import uuid
import os
from urllib.parse import unquote

app = Flask(__name__)

@app.get("/<path:query>")
def download(query):
    # URL-dekodieren (z.B. %20 → Leerzeichen)
    query = unquote(query)

    # Temporäre Datei
    filename = f"{uuid.uuid4()}.mp3"

    # yt-dlp Optionen
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True
    }

    # Suche + Download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        video = info["entries"][0]

    # Datei zurückgeben
    response = send_file(
        filename,
        as_attachment=True,
        download_name=f"{video['title']}.mp3"
    )

    # Datei nach dem Senden löschen
    @response.call_on_close
    def cleanup():
        try:
            os.remove(filename)
        except:
            pass

    return response
