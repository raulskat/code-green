# Project Setup

To set up the environment and run the application:

```bash
cd HackX
pip install -r requirements.txt
python app.py
```

# Continuous Integration

Run the automated test suite with:

```bash
pytest
```

# Directory Overview

- **HackX/templates/** – HTML templates for the Flask views.
- **HackX/static/** – CSS and image assets used by the frontend.
- **HackX/** – Core Python code including the Flask app and detection logic.

# Change Log

- Consolidated duplicate requirements files into a single `requirements.txt`.
- Updated Dockerfile to rely on runtime environment variables.
- Refactored `ai_model.py` and registered an API blueprint in `api.py`.
- Added logging to `app.py` and `rule_model.py`.
- Implemented API key validation for Cohere in `ai_model.py`.
- Added CSRF protection using Flask-WTF.
- Introduced a pytest suite for the rule-based plagiarism checks.

# Future Tasks

- Expand test coverage to the AI module and API endpoints.
- Add caching with Redis to improve performance.
- Implement real-time monitoring of user typing and clipboard activity.
- Document deployment steps using Docker and CI services.
