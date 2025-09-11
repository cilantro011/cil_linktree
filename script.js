// 🌐 Auto-detect API URL: use localhost in dev, Render in prod
const API =
  location.hostname === "localhost"
    ? "http://localhost:5000"
    : "https://cil-spotify-status.onrender.com";

// 🎵 Fetch now-playing info from Flask
async function fetchFlaskData() {
  try {
    const res = await fetch(`${API}/now-playing`);
    const nowPlayingElement = document.getElementById("spotify-now-playing");

    if (res.status === 401) {
      // User not connected yet → show connect link
      nowPlayingElement.innerHTML = `
        <strong>Not connected.</strong>
        <a href="${API}/login" style="margin-left:8px; color:#00ffcc;">Connect Spotify</a>`;
      return;
    }

    const data = await res.json();

    if (data.song && data.song !== "No song playing") {
      let currentSong = data.song; // declared properly
      nowPlayingElement.innerHTML = `<strong>Now Playing:</strong> ${data.song} - ${data.artist}`;
    } else {
      nowPlayingElement.innerHTML = `<strong>No song playing</strong>`;
    }
  } catch (error) {
    console.error("error fetching data:", error);
    const nowPlayingElement = document.getElementById("spotify-now-playing");
    nowPlayingElement.innerHTML = `<strong>Error connecting to server</strong>`;
  }
}

// 🚀 Run immediately + poll every 3 seconds
fetchFlaskData();
setInterval(fetchFlaskData, 3000);
