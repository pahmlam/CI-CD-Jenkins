# ======================
# Base image
# ======================
FROM python:3.13-slim

# ======================
# Set working directory
# ======================
WORKDIR /app


# ======================
# Copy requirements and install dependencies
# ======================
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# ======================
# Copy source code
# ======================
COPY src/train_model.py .
COPY src/app.py .


# ======================
# Train model during build
# ======================
RUN python train_model.py


# ======================
# Expose FastAPI port
# ======================
EXPOSE 8000


# ======================
# Run FastAPI application
# ======================
CMD [ "uvicorn","app:app","--host", "0.0.0.0","--port", "8000"]

