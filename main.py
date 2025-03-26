from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from fastapi import FastAPI, UploadFile, File
import speech_recognition as sr

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the homepage
@app.get("/", response_class=FileResponse)
def serve_home():
    return FileResponse("static/index.html")


@app.get("/")
def read_root():
    return {"message": "EchoAid is alive!"}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    audio_file = await file.read()

    with open("temp.wav", "wb") as f:
        f.write(audio_file)

    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return {"transcription": text}
    except sr.UnknownValueError:
        return {"error": "Could not understand the audio"}
    except sr.RequestError:
        return {"error": "Speech recognition service not available"}
