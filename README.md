# Final Project - Emotion Detector

This Final Project is an AI-based web application that detects emotions from user
text with IBM Watson NLP, packages the detector as a Python module, exposes it
through Flask, and includes unit tests plus static analysis support for the IBM
final project workflow.

## Setup

```bash
pip install -r requirements.txt
python -m unittest test_emotion_detection.py
python server.py
```

## Project Structure

- `EmotionDetection/` contains the package and emotion detector logic.
- `server.py` exposes the Flask application.
- `test_emotion_detection.py` contains unit tests.
- `templates/` and `static/` provide the web UI.
