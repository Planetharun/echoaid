from fastapi import FastAPI, UploadFile, File
import speech_recognition as sr

app = FastAPI()

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
