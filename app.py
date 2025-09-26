from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import autochord # Now we import the actual library
import os

app = FastAPI(title="AutoChord API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Analyzes an uploaded audio file using autochord and returns musical features.
    """
    print(f"Received file: {file.filename}, content-type: {file.content_type}")
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Please upload an audio file (MP3/WAV)")
    
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    
    try:
        # Write file to disk
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Perform actual audio analysis using autochord
        chords_data = autochord.recognize(temp_path)
        
        # Format the chords data
        chords = []
        for start_time, end_time, chord_name in chords_data:
            chords.append({
                "start": round(start_time, 2),
                "end": round(end_time, 2), 
                "chord": chord_name,
                "confidence": 1.0 # autochord doesn't provide confidence, so we use 1.0
            })
        
        # For BPM, key_signature, style, we'll use placeholder values for now.
        # Real implementation would require more libraries (e.g., librosa)
        # which are already dependencies of autochord, but direct calls aren't exposed.
        return {
            "chords": chords,
            "bpm": 120, # Placeholder
            "key_signature": "C Major", # Placeholder
            "musical_style": "Detected", # Placeholder
            "analysis_notes": "Live analysis from AutoChord service (chords only)."
        }
        
    except Exception as e:
        # Catch any errors during analysis and return a 500
        raise HTTPException(status_code=500, detail=f"Analysis failed on server: {str(e)}")
    
    finally:
        # Ensure the temporary file is removed
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
def health_check():
    """A simple endpoint to check if the service is running."""
    return {"status": "healthy", "service": "autochord-api"}

@app.get("/")
def root_check():
    """Root endpoint to show the API is alive."""
    return {"message": "AutoChord API is running and ready for analysis."}
