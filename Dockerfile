FROM python:3.9-slim

WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app files
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]