from fastapi import FastAPI, UploadFile
from main import transcribe_audio
import tempfile

app = FastAPI()

@app.get('/')
def root():
  return {"Hello": "World"}

@app.post('/transcribe')
def transcribe(file: UploadFile):
  with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
    result = transcribe_audio.remote(f.name)
  return {"text": result}

