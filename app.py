from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import autochord, tempfile, shutil, os

API_KEY = os.getenv("AUTOCHORD_API_KEY")  # we’ll set this later

app = FastAPI()

@app.post("/analyze-chords")
async def analyze_audio(file: UploadFile = File(...), authorization: str = 
Header(None)):
    # check the key
    if API_KEY and authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # save the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # run AutoChord
    chords = autochord.recognize(tmp_path)

    return {"chords": chords, "bpm": None}


