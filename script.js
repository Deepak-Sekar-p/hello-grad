const apiUrl = 'https://raw.githubusercontent.com/Deepak-Sekar-p/hello-grad/main/data/uk_postcodes.json';

fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();  // Parse JSON response
    })
    .then(data => {
        if (data && data.length > 0) {
            data.forEach(postcode => {
                if (postcode.latitude && postcode.longitude) {
                    L.marker([postcode.latitude, postcode.longitude])
                        .addTo(map)
                        .bindPopup(`<b>${postcode.postcode}</b><br>${postcode.admin_district}`);
                }
            });
            document.getElementById('status-message').innerText = 'Postcode data loaded successfully!';
        } else {
            document.getElementById('status-message').innerText = 'No postcode data available.';
        }
    })
    .catch(error => {
        console.error('Error fetching postcode data:', error);
        document.getElementById('status-message').innerText = 'Failed to load postcode data.';
    });
