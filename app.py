from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AutoChord API")

# This is CRUCIAL for allowing your Base44 app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all websites to connect
    allow_methods=["*"], # Allows all HTTP methods
    allow_headers=["*"], # Allows all headers
)

@app.post("/")
async def analyze_audio_mock(file: UploadFile = File(...)):
    """
    A mock endpoint that returns a fixed response.
    This helps verify the connection without running the complex autochord library.
    """
    print(f"Received file: {file.filename}, content-type: {file.content_type}")
    
    # We are not processing the file, just confirming we received it.
    
    return {
        "chords": [
            {"start": 0.5, "end": 2.1, "chord": "Am", "confidence": 0.95},
            {"start": 2.1, "end": 4.0, "chord": "G", "confidence": 0.92}
        ],
        "bpm": 125,
        "key_signature": "A Minor",
        "musical_style": "Test Response",
        "analysis_notes": "This is a mock response from the stabilized Railway API. The connection is working!"
    }

@app.get("/health")
def health_check():
    """A simple endpoint to check if the service is running."""
    return {"status": "healthy", "service": "autochord-api"}

@app.get("/")
def root_check():
    """Root endpoint to show the API is alive."""
    return {"message": "AutoChord API is running and ready for analysis."}
