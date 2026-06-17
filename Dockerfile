# Build Stage
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (needed for reflex build)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Initialize reflex (ensures .web and npm packages)
RUN reflex init

# Export the frontend
# Note: In prod, we usually want API_URL to point to the backend's own URL.
# Since we are using a single container, API_URL is the container's own public URL.
# We'll set this via an ARGS/ENV at build time or use a runtime proxy.
RUN reflex export --frontend-only --no-zip

# Runner Stage
FROM python:3.11-slim as runner

WORKDIR /app

# Copy python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the app and the built static files
COPY . .
COPY --from=builder /app/.web/_static /app/static

# Expose the ports (8000 for backend, 3000 for frontend if we ran it, but we'll use a single port)
# In production with reflex run --env prod, it only runs the backend.
# To serve both from one container, we use --backend-only and serve static files via FastAPI.
# Reflex 0.4.x+ doesn't serve the frontend automatically in prod mode.
# We'll add a small entry point or use reflex's built-in static serving if available.

# Alternatively, I'll recommend the TWO-SERVICE layout but with two web services.
# Let's adjust the recommendation to be simpler.

CMD ["reflex", "run", "--env", "prod", "--backend-only"]
