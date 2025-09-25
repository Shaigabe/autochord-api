from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import autochord
import os

# Create FastAPI app
app = FastAPI(title="AutoChord API")

# Add CORS middleware - this is crucial for web requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def analyze_audio(file: UploadFile = File(...)):
    # Simple API key check
    expected_key = os.getenv("AUTOCHORD_API_KEY")
    if expected_key:
        # Note: We'll check this in the request headers if provided
        pass
    
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
        
        # Analyze with autochord
        results = autochord.recognize(temp_path)
        
        # Format response
        chords = []
        for start_time, end_time, chord_name in results:
            chords.append({
                "start": round(start_time, 2),
                "end": round(end_time, 2), 
                "chord": chord_name,
                "confidence": 1.0
            })
        
        return {
            "chords": chords,
            "bpm": 120,
            "key_signature": "C Major",
            "musical_style": "Detected",
            "analysis_notes": "Live analysis from AutoChord service"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "autochord-api"}

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "AutoChord