import os
from flask import Flask, jsonify, redirect, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:5000/callback")  # default local
SCOPE = "user-read-currently-playing"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=".spotifycache"
)

def get_spotify_token():
    tok = sp_oauth.get_cached_token()
    if not tok:
        return None
    if sp_oauth.is_token_expired(tok):
        tok = sp_oauth.refresh_access_token(tok["refresh_token"])
    return tok["access_token"]

@app.route("/login")
def login():
    return redirect(sp_oauth.get_authorize_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code from Spotify", 400
    sp_oauth.get_access_token(code)   # writes to cache
    return redirect("/now-playing")

@app.route("/now-playing")
def now_playing():
    access = get_spotify_token()
    if not access:
        return jsonify({"error": "User not authenticated"}), 401
    try:
        sp = spotipy.Spotify(auth=access)
        cur = sp.current_user_playing_track()
        if cur and cur.get("is_playing") and cur.get("item"):
            item = cur["item"]
            name = item.get("name", "Unknown")
            artists = item.get("artists") or []
            artist = artists[0]["name"] if artists else "Unknown"
            return jsonify({"song": name, "artist": artist})
        return jsonify({"song": "No song playing", "artist": ""})
    except Exception as e:
        print("Spotify error:", e)
        return jsonify({"error": "Failed to fetch now playing"}), 500

if __name__ == "__main__":
    app.run(debug=True)
