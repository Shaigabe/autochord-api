from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import autochord
import os

# --- Security ---
API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
EXPECTED_API_KEY = os.getenv("AUTOCHORD_API_KEY")

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if not EXPECTED_API_KEY:
        # If no server-side key is set, we can allow access, but it's less secure.
        # For this setup, we'll enforce the key check.
        raise HTTPException(status_code=500, detail="API Key not configured on server")
    if not api_key_header:
        raise HTTPException(status_code=403, detail="Authorization header missing")
    
    try:
        scheme, _, key = api_key_header.partition(' ')
        if scheme.lower() != 'bearer' or key != EXPECTED_API_KEY:
            raise HTTPException(status_code=403, detail="Invalid API Key or scheme")
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")

# --- App Initialization ---
app = FastAPI(
    title="AutoChord API",
    description="Analyzes audio files to extract chords and musical features.",
    version="1.0.0"
)

# --- CORS Middleware ---
# This is the crucial part that allows your Base44 app to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods
    allow_headers=["*"], # Allows all headers
)

# --- API Endpoints ---
@app.post("/")
async def analyze_chords(file: UploadFile = File(...), _ = Depends(get_api_key)):
    if not file.content_type in ["audio/mpeg", "audio/wav", "audio/x-wav"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload MP3 or WAV.")

    temp_file_path = f"/tmp/{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        chords_data = autochord.recognize(temp_file_path)
        
        chords = [
            {"start": round(start, 2), "end": round(end, 2), "chord": name, "confidence": 1.0}
            for start, end, name in chords_data
        ]
        
        # Placeholder values for other features, to match the frontend's expectations
        return {
            "chords": chords,
            "bpm": 120,
            "key_signature": "C Major",
            "musical_style": "Pop",
            "analysis_notes": "Analysis from live AutoChord service."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/health")
def health_check():
    return {"status": "ok"}