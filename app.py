import whisper

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

print("Loading Whisper model...")

model = whisper.load_model("base")

print("Model loaded!")

file_path = "video.mp4"

print("Generating subtitles...")

result = model.transcribe(file_path)

segments = result["segments"]

with open("subtitles.srt", "w") as srt_file:

    for i, segment in enumerate(segments, start=1):

        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()

        srt_file.write(f"{i}\n")
        srt_file.write(f"{start} --> {end}\n")
        srt_file.write(f"{text}\n\n")

print("Subtitle file generated successfully!")