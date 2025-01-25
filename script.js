// Define the API URL to fetch postcode data from the GitHub raw content URL
const apiUrl = 'https://raw.githubusercontent.com/Deepak-Sekar-p/hello-grad/main/data/uk_postcodes.json';

// Initialize the map centered around the UK
const map = L.map('map').setView([51.509865, -0.118092], 6);

// Load and display OpenStreetMap tiles on the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Function to fetch and load postcode data from GitHub
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
