FROM python:3.11-slim

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
