FROM python:3.11-slim

# Install system dependencies for PDF conversion
RUN apt-get update && apt-get install -y \
    libreoffice \
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for generated reports
RUN mkdir -p /app/reports

# Run the bot
CMD ["python", "bot.py"]