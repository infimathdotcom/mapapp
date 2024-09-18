# Stage 1: Builder stage
FROM python:3.11-alpine AS builder

# Install necessary build dependencies for Alpine
RUN apk add --no-cache gcc musl-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies in the builder stage
COPY requirements.txt .

# Install dependencies in the builder stage
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-alpine

# Set the working directory
WORKDIR /

# Copy only the installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY ./app /app

# Expose the port
EXPOSE 80

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
