# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /workspace

# Install system dependencies needed for machine learning libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core application code into the container
COPY ./app /workspace/app

# Expose port 8000 for network access
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

