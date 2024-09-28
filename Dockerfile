# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask or any other Python web framework you might use
EXPOSE 5000

# Define environment variable for Python to not buffer stdout/stderr
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
