# AI-Powered Subtitle Generator

An AI-based subtitle generation system that converts audio/video speech into subtitles using OpenAI Whisper.

The project includes:
- Streamlit frontend
- FastAPI backend
- Chrome extension
- FFmpeg audio processing
- Multi-language transcription
- Subtitle (.srt) generation

---

# Features

- Audio transcription
- Video transcription
- Automatic subtitle generation
- Downloadable `.srt` files
- Multi-language support
- Browser audio capture
- FastAPI REST API
- Chrome extension integration
- Whisper AI speech recognition

---

# Tech Stack

## Frontend
- Streamlit
- HTML
- CSS
- JavaScript

## Backend
- FastAPI
- Python

## AI / Audio Processing
- OpenAI Whisper
- FFmpeg

## Browser Extension
- Chrome Extension APIs
- MediaRecorder API

---



# Supported Formats

Audio
mp3
wav

Video
mp4
mov
mkv


# Run Commands

## Activate Virtual Environment

### Mac/Linux

```bash
source venv/bin/activate


## Run Streamlit frontend

streamlit run streamlit_app.py
frontend url: http://localhost:8501

## Run FastAPI Backend

uvicorn api:app --reload

Backend URL:

http://127.0.0.1:8000

API Docs:

http://127.0.0.1:8000/docs




# Project Architecture

```text
                ┌────────────────────┐
                │   Streamlit UI     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   FastAPI Backend  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   OpenAI Whisper   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Subtitle Generation│
                └────────────────────┘

