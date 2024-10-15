document.getElementById('recommendation-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const preferredGenre = document.getElementById('preferred-genre').value;
    const lastReadManga = document.getElementById('last-read-manga').value;
    const completeSeries = document.getElementById('complete-series').value;
  
    fetch('/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        preferred_genre: preferredGenre,
        last_read_manga: lastReadManga,
        complete_series: completeSeries
      })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('recommendation-output').innerText = `Recommendation: ${data.recommendation}`;
    })
    .catch(error => console.error('Error:', error));
  });  