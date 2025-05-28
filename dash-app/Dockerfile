# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (optional: gcc for some pip packages)
RUN apt-get update && apt-get install -y gcc

# Copy the requirements.txt (if you have one)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your Dash app runs on
EXPOSE 8050

# Run modelos.py first, then app.py
CMD python analise/modelos.py && python dash_app.py