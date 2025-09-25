# Use a Python 3.11 base image, which is compatible with TensorFlow 2.15
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies needed for sound processing and build tools
# ffmpeg for librosa, build-essential for compiling some Python packages
# libsndfile1 for soundfile
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel for better dependency resolution
RUN pip install --upgrade pip setuptools wheel

# Install numpy first, as some packages (like librosa/autochord dependencies)
# might try to build against it and fail if it's not present.
RUN pip install numpy==1.26.4

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the rest of the Python dependencies from requirements.txt
# --no-cache-dir reduces image size
# --no-build-isolation is often useful in Docker builds
RUN pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Copy the rest of your application code (e.g., app.py) into the container
COPY . .

# Expose the port that your FastAPI application will listen on
EXPOSE 8000

# Set the VAMP_PATH environment variable for autochord (optional, but good practice)
# This is where VAMP plugins are typically located in a Debian-based system
ENV VAMP_PATH=/usr/lib/vamp

# Command to run your FastAPI application with Uvicorn
# The app.py file defines the 'app' FastAPI instance
# --host 0.0.0.0 makes it accessible from outside the container
# --port 8000 (Railway will map this to an external port)
CMD ["uvicorn", "app:app", "--host