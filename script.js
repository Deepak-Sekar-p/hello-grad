// Define the API URL to fetch postcode data from GitHub raw content
const apiUrl = 'https://raw.githubusercontent.com/Deepak-Sekar-p/hello-grad/main/data/uk_postcodes.json';

// Initialize the map centered around the UK
const map = L.map('map').setView([55.3781, -3.4360], 6); // Centered on the UK

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
        return response.json();  // Convert response to JSON
    })
    .then(data => {
        if (data && data.length > 0) {
            data.forEach(postcode => {
                // Ensure latitude and longitude exist before adding markers
                if (postcode.latitude && postcode.longitude) {
                    L.marker([postcode.latitude, postcode.longitude])
                        .addTo(map)
                        .bindPopup(
                            `<b>Postcode:</b> ${postcode.postcode}<br>` +
                            `<b>Country:</b> ${postcode.country}<br>` +
                            `<b>Region:</b> ${postcode.region || 'N/A'}<br>` +
                            `<b>Admin District:</b> ${postcode.admin_district || 'N/A'}<br>` +
                            `<b>Longitude:</b> ${postcode.longitude}<br>` +
                            `<b>Latitude:</b> ${postcode.latitude}`
                        );
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
