# Base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Copy the .env file if it is needed by the app
COPY .env /app/.env

# Expose the application port
EXPOSE 5000

# Command to start the app
CMD ["flask", "run", "--host=0.0.0.0", "--port", "5000"]
