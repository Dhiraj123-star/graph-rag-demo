# Use slim Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system deps (for faiss + numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache optimisation)
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run app
CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]