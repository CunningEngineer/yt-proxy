from flask import Flask, request, redirect, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/youtube/play")
def youtube():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.txt")

    ydl_opts = {
        "format": "best",
        "quiet": True,
        "noplaylist": True,
        "cookiefile": cookie_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return redirect(info["url"], code=302)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
