FROM python:3.10-slim

WORKDIR /app

# Install build tools (optional but useful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

EXPOSE 5000

# Run with Gunicorn (faster, more stable)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
