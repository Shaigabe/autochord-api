FROM python:3.10-slim

# Install system dependencies needed for audio processing libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip to the latest version as recommended by the logs
RUN pip install --upgrade pip

# Install numpy first to prevent build issues with other dependencies
RUN pip install numpy==1.26.4 --no-cache-dir

# Copy and install remaining Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
