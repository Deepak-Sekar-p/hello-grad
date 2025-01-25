var map = L.map('map').setView([54.5, -2], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

fetch('https://your-backend-url/api/postcodes')
    .then(response => response.json())
    .then(data => {
        data.data.forEach(area => {
            let geoJson = L.geoJSON(area.boundary, {
                style: { color: "#3388ff", weight: 2 },
                onEachFeature: function (feature, layer) {
                    layer.on('mouseover', function () {
                        layer.setStyle({ color: "yellow" });
                        layer.bindPopup(`<b>Postcode:</b> ${area.postcode}<br>Lat: ${area.latitude}, Lon: ${area.longitude}`).openPopup();
                    });
                    layer.on('mouseout', function () {
                        layer.setStyle({ color: "#3388ff" });
                        layer.closePopup();
                    });
                }
            }).addTo(map);
        });
    })
    .catch(error => console.error('Error:', error));
