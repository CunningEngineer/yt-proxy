from flask import Flask, request, redirect, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/youtube/play")
def youtube():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio/best[ext=webm]/best[ext=mp4]/best",
        "quiet": True,
        "noplaylist": True,
        "cookiefile": "cookies.txt",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return redirect(info["url"], code=302)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
