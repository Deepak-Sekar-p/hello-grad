hello-grad-webapp/
│-- .github/                     # GitHub Actions workflow directory
│   └── workflows/
│       └── update_postcodes.yml  # GitHub workflow to auto-update postcode data
│
│-- backend/                      # Backend (FastAPI)
│   ├── main.py                    # FastAPI app to serve postcode data
│   ├── requirements.txt            # Dependencies for backend
│   └── update_data.py               # Script to fetch and update postcode data
│
│-- frontend/                      # Frontend (HTML, CSS, JS)
│   ├── index.html                  # Frontend UI
│   ├── style.css                    # CSS styles for the map (optional)
│   └── script.js                     # JavaScript to fetch and render postcode data
│
│-- data/                          # Data storage directory
│   └── uk_postcodes.json            # Postcode data file (auto-updated via GitHub Actions)
│
│-- .gitignore                      # Ignore unnecessary files
│-- README.md                        # Project documentation
