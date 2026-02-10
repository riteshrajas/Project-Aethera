# Project Aethera

**Project Aethera is the successor to Pyintel, an AI created by Ritesh.**

This project aims to be the next biggest advancement in AI, creating a powerful and useful AI system with multi-point control. It will be capable of doing everything from building AI-powered applications to rating entire databases using only voice commands. Project Aethera is designed as a personal assistant that learns on command, drawing inspiration from capabilities like Iron Man's J.A.R.V.I.S. and general AI wrapper functionalities.

## Features
See `Aethera_Features.md` for a detailed list of planned features.

## Setup
1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment:
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file from `.env.example` (if provided) and add your API keys and other configurations.
6.  Run the application: `python main.py`

## Web Client
Run the lightweight web client to analyze text from a browser:

1.  Start the server: `python -m services.web_client`
2.  Open `http://localhost:5000` in your browser.

Note: This runs Flask's development server for local use. Use a production WSGI server (e.g., gunicorn or waitress) for deployments.

## Project Structure
(A brief overview of the main directories)
- `core/`: Core J.A.R.V.I.S.-like functionalities.
- `wrapper/`: AI wrapper functionalities.
- `utils/`: Utility functions.
- `config/`: Configuration files.
- `tests/`: Unit and integration tests.
- `docs/`: Project documentation.
- `main.py`: Main application entry point.
