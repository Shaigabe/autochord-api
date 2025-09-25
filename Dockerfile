FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy==1.26.4

COPY requirements.txt .
RUN pip install --no-build-isolation -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM 
python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and preinstall numpy
RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy==1.26.4

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-build-isolation -r requirements.txt

# Copy the rest of your project (app.py, etc.)
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# Use a stable Python base image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and preinstall numpy
RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy==1.26.4

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-build-isolation -r requirements.txt

# Copy the rest of your project (app.py, etc.)
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]





# Use a 
stable 
Python base 
image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and preinstall numpy
RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy==1.26.4

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-build-isolation -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM 
python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy==1.26.4

COPY requirements.txt .
RUN pip install --no-build-isolation -r requirements.

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "0"]
