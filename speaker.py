# Install the assemblyai package by executing the command `pip3 install assemblyai` (macOS) or `pip install assemblyai` (Windows).

# Import the AssemblyAI module
import assemblyai as aai

# Import Recording module
import tempfile
import os
import sounddevice as sd
from scipy.io.wavfile import write

def speech_to_text(duration,fs:int = 16000) -> str:
    # Your API token is already set here
    aai.settings.api_key = "91ff0567d6314bdba344fc0c9f220571"

    # Create a transcriber object.
    transcriber = aai.Transcriber()

    # Record
    print("Recording")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')

    sd.wait()

    # Saving file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                write(tmpfile.name, fs, recording)
                audio_path = tmpfile.name

    # If you have a local audio file, you can transcribe it using the code below.
    # Make sure to replace the filename with the path to your local audio file.
    print("Transcribting...")
    transcript = transcriber.transcribe(audio_path  )

    # Alternatively, if you have a URL to an audio file, you can transcribe it with the following code.
    # Uncomment the line below and replace the URL with the link to your audio file.
    # transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/espn-bears.m4a")

    # After the transcription is complete, the text is printed out to the console.
    return transcript.text

if __name__ == "__main__":
        result = speech_to_text(5)
        print(result)

# Assembly giới hạng 50 đồng biden mỗi tài khoản free, sài tiết kiệm please và dùng key của tao, nếu hết hạn thì sài key của tụi bây
