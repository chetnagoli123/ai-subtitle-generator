from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import whisper
import shutil
import os
import subprocess

# -----------------------------
# Create FastAPI app
# -----------------------------
app = FastAPI()

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load Whisper model once
# -----------------------------
model = whisper.load_model("tiny")


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():

    return {
        "message": "AI Subtitle API Running"
    }


# -----------------------------
# Transcription Route
# -----------------------------
@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...)
):

    try:

        # -----------------------------
        # Temporary filenames
        # -----------------------------
        input_filename = "temp_chunk.webm"

        output_filename = "temp_audio.wav"

        # -----------------------------
        # Save uploaded chunk
        # -----------------------------
        with open(input_filename, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # -----------------------------
        # Convert webm → wav
        # -----------------------------
        ffmpeg_command = [

            "ffmpeg",
            "-y",
            "-i",
            input_filename,

            "-vn",

            "-acodec",
            "pcm_s16le",

            "-ar",
            "16000",

            "-ac",
            "1",

            output_filename
        ]

        result = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True
        )

        # -----------------------------
        # Check conversion success
        # -----------------------------
        if result.returncode != 0:

            return {
                "error": result.stderr
            }

        if not os.path.exists(output_filename):

            return {
                "error": "Audio conversion failed"
            }

        # -----------------------------
        # Whisper transcription
        # -----------------------------
        transcript_result = model.transcribe(
            output_filename
        )

        transcript_text = transcript_result["text"]

        # -----------------------------
        # Cleanup files
        # -----------------------------
        if os.path.exists(input_filename):

            os.remove(input_filename)

        if os.path.exists(output_filename):

            os.remove(output_filename)

        # -----------------------------
        # Return transcript
        # -----------------------------
        return {
            "transcript": transcript_text
        }

    except Exception as e:

        return {
            "error": str(e)
        }