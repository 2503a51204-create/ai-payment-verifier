# ProofOfReality AI

THINK BEYOND 2026 hackathon prototype for digital-evidence risk assessment.

## Features

- Direct image/PDF upload
- SHA-256 digital fingerprint
- PDF text extraction
- Optional image OCR with Tesseract
- Basic metadata/type/size reporting
- Risk-indicator assessment
- Trust score
- SQLite verification history
- Responsive HTML/CSS/JavaScript dashboard

## Project structure

```text
ProofOfReality/
├── app.py
├── requirements.txt
├── README.md
├── run.bat
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── services/
│   ├── __init__.py
│   └── analyzer.py
├── utils/
│   ├── __init__.py
│   └── database.py
├── uploads/
├── database/
└── docs/
    └── PROJECT_FLOW.txt
```

## Run on Windows

1. Install Python 3.10+.
2. Open PowerShell in this folder.
3. Run:
   `python -m pip install -r requirements.txt`
4. Run:
   `python app.py`
5. Open:
   `http://127.0.0.1:5000`

## Important

The image OCR feature requires the Tesseract OCR application to be installed and available on PATH.

This project is a hackathon prototype. Its output is a risk assessment, not definitive forensic proof that a file is authentic or fake.

Mandana AI is not claimed as integrated in this ZIP because an official API/SDK and credentials would be required for a real integration.
