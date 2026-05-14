let mediaRecorder;

let audioChunks = [];

document
    .getElementById("startBtn")
    .addEventListener("click", async () => {

        try {

            document.getElementById("status")
                .innerText =
                "Requesting tab audio...";

            const stream =
                await navigator.mediaDevices.getDisplayMedia({

                    video: true,
                    audio: true
                });

            audioChunks = [];

            mediaRecorder =
                new MediaRecorder(stream);

            mediaRecorder.ondataavailable =
                (event) => {

                    if (event.data.size > 0) {

                        audioChunks.push(event.data);
                    }
                };

            mediaRecorder.onstop =
                async () => {

                    try {

                        document.getElementById("status")
                            .innerText =
                            "Processing audio...";

                        // Create ONE proper complete blob
                        const audioBlob =
                            new Blob(
                                audioChunks,
                                {
                                    type: "audio/webm"
                                }
                            );

                        const formData =
                            new FormData();

                        formData.append(
                            "file",
                            audioBlob,
                            "recording.webm"
                        );

                        const response =
                            await fetch(
                                "http://127.0.0.1:8000/transcribe",
                                {
                                    method: "POST",
                                    body: formData
                                }
                            );

                        const data =
                            await response.json();

                        console.log(data);

                        document.getElementById("status")
                            .innerText =
                            data.transcript || data.error;

                    } catch (error) {

                        console.error(error);

                        document.getElementById("status")
                            .innerText =
                            "Transcription failed";
                    }
                };

            mediaRecorder.start();

            document.getElementById("status")
                .innerText =
                "Recording started";

        } catch (error) {

            console.error(error);

            document.getElementById("status")
                .innerText =
                "Failed to capture audio";
        }
    });


document
    .getElementById("stopBtn")
    .addEventListener("click", () => {

        if (mediaRecorder &&
            mediaRecorder.state !== "inactive") {

            mediaRecorder.stop();

            document.getElementById("status")
                .innerText =
                "Stopping recording...";
        }
    });