from flask import Flask, jsonify, session, redirect, request
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "sajan"
app.config["SESSION_COOKIE_NAME"] = "Spotify Login"

#Spotify API credentials
SPOTIPY_CLIENT_ID = "4520adbd1d724a10bd386fb6fc818f7d"
SPOTIPY_CLIENT_SECRET = "62b2420df69345c1a0f5887ba7e950d4"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/now-playing"


#setup authentication
sp_oauth = SpotifyOAuth(
    client_id = SPOTIPY_CLIENT_ID,
    client_secret = SPOTIPY_CLIENT_SECRET,
    redirect_uri = SPOTIPY_REDIRECT_URI,
    scope = "user-read-currently-playing",
    cache_path = ".spotifycache"
)


def get_spotify_token():
    """Retrieve or refresh the Spotify access token, saving it to a file."""
    if not os.path.exists(".spotifycache"):
        return None  # ✅ If cache file doesn't exist, user needs to log in.

    try:
        with open(".spotifycache", "r") as f:
            token_info = json.load(f)  # ✅ Read token from file
    except json.JSONDecodeError:
        return None  # ✅ If file is corrupt, user needs to log in.

    # Check if the token has expired
    if time.time() > token_info["expires_at"]:
        print("Access token expired. Refreshing...")
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        with open(".spotifycache", "w") as f:
            json.dump(token_info, f)  # ✅ Save refreshed token

    return token_info["access_token"]




@app.route('/now-playing')
def now_playing():
    access_token = get_spotify_token()
    
    if not access_token:
        return jsonify({"error": "User not authenticated"}), 401
    
    sp = spotipy.Spotify(auth=access_token)
    
    current_track = sp.current_user_playing_track()
    
    if current_track and current_track['is_playing']:
        song_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        return jsonify({"song": song_name, "artist": artist_name})
    else:
        return jsonify({"song": "No song playing", "artist": ""})
    

@app.route('/login')
def login():
    return redirect(sp_oauth.get_authorize_url())

@app.route('/callback')
def spotify_callback():
    session.clear()
    code = request.args.get("code")
    
    if not code:
        return "Error: No code received from Spotify!", 400
    
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect('/now-playing')


if __name__=="__main__":
    app.run(debug=True)