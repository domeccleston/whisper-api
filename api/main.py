from modal import Image, Stub, asgi_app, Secret
from fastapi import FastAPI, UploadFile, Header
import unkey
from tempfile import NamedTemporaryFile
import os 

# import os
# import cloudpickle

app_image = (
    Image.debian_slim()
    .pip_install(
        "openai-whisper",
        "dacite",
        "jiwer",
        "ffmpeg-python",
        "gql[all]~=3.0.0a5",
        "pandas",
        "loguru==0.6.0",
        "torchaudio==0.12.1",
        "yt-dlp",
        "unkey.py",
        "python-dotenv",
        "psycopg2-binary"
    )
    .apt_install("ffmpeg")
    .pip_install("ffmpeg-python")
)

web_app = FastAPI()

stub = Stub(
    "whisper-audio-video-transcriber-api-v2",
    image=app_image,
)

@web_app.post("/transcribe")
async def transcribe(file: UploadFile, authorization: str = Header(None)):
  import unkey
  import os
  from dotenv import load_dotenv
  import whisper
  import psycopg2

  load_dotenv()

  # Authorize request using Unkey

  if not authorization:
    return { "error": "Must supply API key in Authorization header." }
  else:
    schema, _, token = authorization.partition(" ")

  client = unkey.Client(api_key=os.environ["unkey_root_key"])

  await client.start()

  result = await client.keys.verify_key(token, api_id=os.environ["unkey_api_id"])

  await client.close()

  if not result.is_ok:
    result = result.unwrap_err()
    print("not ok")
    return { "Error": "Error verifying key." }
  else:
    data = result.unwrap()
    if not data.valid:
        return { "Error": "Invalid key." }
    
    # Create temporary file to run Whisper on
    with NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Transcribe audio
    model = whisper.load_model("base")
    result = model.transcribe(temp_file_path)

    # Save result to database
    # TODO: get the original filename from the request
    connection_string = os.getenv("database_url")
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transcripts (filename, transcript) VALUES (%s, %s) RETURNING id;", (file.filename, result['text']))
    id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return { "result": f'Transcribed audio file successfully. Access it at https://modal-roan.vercel.app/{id}.' }

@stub.function(image=app_image, secret=Secret.from_name("unkey_api_key"))
@asgi_app()
def fastapi_app():
    return web_app
