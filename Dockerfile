FROM python:latest

# Create app directory
WORKDIR /app

# Install requirements first (improves caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask server
CMD ["python", "server.py"]
