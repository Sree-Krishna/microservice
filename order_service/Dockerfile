# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8001

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
