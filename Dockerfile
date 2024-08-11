# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies for Python
RUN pip install --no-cache-dir poetry

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm

# Install TypeScript globally
RUN npm install -g typescript

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Install Python project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy package.json and package-lock.json (if available) for Node.js dependencies
COPY package*.json /app/

# Install Node.js project dependencies
RUN npm install

# Copy the project files
COPY . /app/

# Ensure the static files are collected
RUN poetry run python manage.py collectstatic --noinput

# Compile TypeScript files (if needed)
RUN tsc

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
