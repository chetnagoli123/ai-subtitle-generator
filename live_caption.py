import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os

# Load Whisper model
model = whisper.load_model("base")

sample_rate = 16000
duration = 5  # seconds

print("Live caption system started...\n")

while True:

    print("Listening...")

    # Record audio
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )

    sd.wait()

    # Temporary audio file
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    sf.write(temp_file.name, recording, sample_rate)

    # Transcribe
    result = model.transcribe(temp_file.name)

    print("\nCaption:")
    print(result["text"])
    print("-" * 50)

    # Cleanup
    os.remove(temp_file.name)