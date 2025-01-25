// Initialize the map with a center point (UK coordinates)
const map = L.map('map').setView([51.509865, -0.118092], 6);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Replace with your deployed backend API URL
const apiUrl = 'https://your-backend-api-url/api/postcodes';

// Function to fetch postcode data from the backend API
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        document.getElementById('status-message').innerText = 'Postcode data loaded successfully!';
        
        if (data.data && data.data.length > 0) {
            data.data.forEach(postcode => {
                if (postcode.latitude && postcode.longitude) {
                    L.marker([postcode.latitude, postcode.longitude])
                        .addTo(map)
                        .bindPopup(`<b>${postcode.postcode}</b><br>${postcode.admin_district}`);
                }
            });
        } else {
            document.getElementById('status-message').innerText = 'No postcode data available.';
        }
    })
    .catch(error => {
        console.error('Error fetching postcode data:', error);
        document.getElementById('status-message').innerText = 'Failed to load postcode data.';
    });
