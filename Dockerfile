# Use a lightweight official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy backend code and ML model
COPY backend/ ./backend/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose the Flask port
EXPOSE 5001

# Run the Flask app
CMD ["python", "backend/app.py"]
