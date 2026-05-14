import streamlit as st
import whisper
import yt_dlp
import time

# -----------------------------
# Timestamp formatting function
# -----------------------------
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


# -----------------------------
# Download YouTube Audio
# -----------------------------
def download_youtube_audio(url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'youtube_audio.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

    return filename


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("AI Subtitle Generator")

st.write("Upload audio/video or paste a YouTube URL.")


# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["mp3", "wav", "mp4", "mov", "mkv"]
)


# -----------------------------
# YouTube URL Input
# -----------------------------
youtube_url = st.text_input(
    "Or Paste YouTube Video URL"
)


# -----------------------------
# Language Selection
# -----------------------------
languages = {
    "Auto Detect": None,
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh"
}

selected_language = st.selectbox(
    "Select Language",
    list(languages.keys())
)

language_code = languages[selected_language]


# -----------------------------
# Whisper Model Selection
# -----------------------------
model_option = st.selectbox(
    "Choose Whisper Model",
    ["tiny", "base", "small", "medium"]
)


# -----------------------------
# Process Input
# -----------------------------
if uploaded_file is not None or youtube_url:

    # -----------------------------
    # Handle Uploaded File
    # -----------------------------
    if uploaded_file is not None:

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())

        file_path = uploaded_file.name

        st.success("File uploaded successfully!")

    # -----------------------------
    # Handle YouTube URL
    # -----------------------------
    elif youtube_url:

        with st.spinner("Downloading YouTube audio..."):

            file_path = download_youtube_audio(youtube_url)

        st.success("YouTube audio downloaded successfully!")

    # -----------------------------
    # Media Preview
    # -----------------------------
    if uploaded_file is not None:

        if uploaded_file.type.startswith("video"):

            st.video(uploaded_file)

        elif uploaded_file.type.startswith("audio"):

            st.audio(uploaded_file)

    # -----------------------------
    # Load Whisper Model
    # -----------------------------
    with st.spinner("Loading Whisper model..."):

        model = whisper.load_model(model_option)

    # -----------------------------
    # Start Timer
    # -----------------------------
    start_time = time.time()

    # -----------------------------
    # Transcription
    # -----------------------------
    with st.spinner("Generating subtitles..."):

        result = model.transcribe(
            file_path,
            language=language_code
        )

    # -----------------------------
    # End Timer
    # -----------------------------
    end_time = time.time()

    processing_time = round(end_time - start_time, 2)

    # -----------------------------
    # Show Transcript
    # -----------------------------
    st.subheader("Transcript")

    st.write(result["text"])

    # -----------------------------
    # Generate Subtitle File
    # -----------------------------
    segments = result["segments"]

    srt_filename = "subtitles.srt"

    with open(srt_filename, "w") as srt_file:

        for i, segment in enumerate(segments, start=1):

            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            srt_file.write(f"{i}\n")
            srt_file.write(f"{start} --> {end}\n")
            srt_file.write(f"{text}\n\n")

    # -----------------------------
    # Success Message
    # -----------------------------
    st.success(
        f"Subtitle file generated successfully in {processing_time} seconds!"
    )

    # -----------------------------
    # Download Button
    # -----------------------------
    with open(srt_filename, "rb") as file:

        st.download_button(
            label="Download Subtitles (.srt)",
            data=file,
            file_name="subtitles.srt",
            mime="text/plain"
        )