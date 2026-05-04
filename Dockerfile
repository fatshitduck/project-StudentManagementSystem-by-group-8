# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for GUI applications
RUN apt-get update && apt-get install -y \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create data directory
RUN mkdir -p data

# Set environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:0

# Expose port if needed (though this is a GUI app)
# EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]