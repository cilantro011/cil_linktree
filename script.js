
async function fetchFlaskData(){
    try {
        const response = await fetch("http://127.0.0.1:5000/now-playing");
        const data = await response.json();
        

        const nowPlayingElement = document.getElementById("spotify-now-playing");

        if (data.song !== "No song playing" ){
            currentSong = data.song; // Update current song
            nowPlayingElement.innerHTML = `<strong>Now Playing:</strong> ${data.song} - ${data.artist}`;
        }
        else {
            nowPlayingElement.innerHTML = `<strong>No song playing</strong>`;
        }
    } catch (error) {
        console.error("error fetching data:", error);
    }
}

fetchFlaskData();

setInterval(fetchFlaskData, 3000);
