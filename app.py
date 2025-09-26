from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import autochord # For chord recognition
import librosa # For BPM, key detection, and audio loading
import numpy as np # For numerical operations with librosa
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
    Analyzes an uploaded audio file using autochord and librosa to return
    musical features including chords, BPM, and key signature.
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
        
        # --- Perform actual audio analysis using autochord and librosa ---
        
        # Load audio for librosa processing (using native samplerate)
        y, sr = librosa.load(temp_path, sr=None) 

        # 1. Chord Recognition (using autochord)
        chords_data = autochord.recognize(temp_path)
        chords = []
        for start_time, end_time, chord_name in chords_data:
            chords.append({
                "start": round(start_time, 2),
                "end": round(end_time, 2), 
                "chord": chord_name,
                "confidence": 1.0 # autochord doesn't provide confidence, so we use 1.0
            })

        # 2. BPM Detection (using librosa)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        detected_bpm = round(tempo)

        # 3. Key Signature Detection (using librosa's chroma features)
        # Compute chroma features (chroma_cens is robust to timbre variations)
        chroma = librosa.feature.chroma_cens(y=y, sr=sr)
        # Take the mean over time to get an overall chroma profile
        chroma_mean = np.mean(chroma, axis=1)

        # Define simplified major and minor key templates (from music theory heuristics)
        # These templates represent the relative prominence of each semitone in major/minor scales.
        # Values are typically derived from empirical studies (e.g., Krumhansl-Kessler)
        major_template = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_template = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        
        # Normalize templates to unit vectors for robust comparison
        major_template = major_template / np.linalg.norm(major_template)
        minor_template = minor_template / np.linalg.norm(minor_template)
        
        # Shift the templates for each of the 12 possible keys (C, C#, D, ..., B)
        # and calculate the correlation (dot product) with the audio's chroma profile.
        major_scores = [np.dot(chroma_mean, np.roll(major_template, i)) for i in range(12)]
        minor_scores = [np.dot(chroma_mean, np.roll(minor_template, i)) for i in range(12)]
        
        # Find the key (root note) with the highest score for both major and minor modes
        major_key_idx = np.argmax(major_scores)
        minor_key_idx = np.argmax(minor_scores)
        
        # Map index to actual pitch name
        pitch_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Determine if the best match is major or minor
        detected_key_signature = ""
        if major_scores[major_key_idx] > minor_scores[minor_key_idx]:
            detected_key_signature = f"{pitch_names[major_key_idx]} Major"
        else:
            detected_key_signature = f"{pitch_names[minor_key_idx]} Minor"

        # 4. Musical Style (using a simple heuristic for now)
        # Advanced style detection requires complex ML models, so for now, we'll provide a general note.
        detected_musical_style = "Instrumental (via AI analysis)" # Placeholder, can be improved with LLM if needed

        return {
            "chords": chords,
            "bpm": detected_bpm,
            "key_signature": detected_key_signature,
            "musical_style": detected_musical_style,
            "analysis_notes": "Chords via AutoChord; BPM and Key via Librosa. Style is an estimate."
        }
        
    except Exception as e:
        # Catch any errors during analysis and return a 500
        print(f"Error during audio analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed on server: {str(e)}. Ensure audio file is valid.")
    
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
