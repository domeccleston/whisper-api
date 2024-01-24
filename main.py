from modal import Image, Stub, Mount, web_endpoint, asgi_app, Secret
from fastapi import FastAPI, Request, UploadFile, Header
from fastapi.responses import HTMLResponse
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
    )
    .apt_install("ffmpeg")
    .pip_install("ffmpeg-python")
)

web_app = FastAPI()

stub = Stub(
    "whisper-audio-video-transcriber-api-v2",
    image=app_image,
)

# @stub.function(image=app_image, mounts=[Mount.from_local_dir("/Users/dominiceccleston/Code/modal/files", remote_path="/etc")])
# def transcribe_audio(file):
#     import whisper
#     model = whisper.load_model('base')
#     result = model.transcribe(file)
#     return result.text

@web_app.post("/transcribe")
async def transcribe(file: UploadFile, authorization: str = Header(None)):
    import whisper

    # "Authorization: Bearer {unkey}"
    if authorization:
        schema, _, token = authorization.partition(' ')

    client = unkey.Client(api_key=os.environ["unkey_api_key"])
    result = await client.keys.verify_key(token)

    if not result.is_ok:
        # handle error
        pass
    
    with NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    model = whisper.load_model("base")
    result = model.transcribe(temp_file_path)
    return { "result": result['text'] }

@stub.function(image=app_image, secret=Secret.from_name("unkey_api_key"))
@asgi_app()
def fastapi_app():
    return web_app
