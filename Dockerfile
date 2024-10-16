# Use a specific version of Python to avoid compatibility issues
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install necessary packages for psycopg
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run your application with Gunicorn or runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
