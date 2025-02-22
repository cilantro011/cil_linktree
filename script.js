async function fetchFlaskData(){
    try {
        const response = await fetch("http://127.0.0.1:5000/");
        const data = await response.json();

        document.getElementById("spotify-now-playing").innerText = data.message;
    } catch (error) {
        console.error("error fetching data:", error);
    }
}

fetchFlaskData();

