FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install dvc

# Copy all project files
COPY . .

# Set PYTHONPATH so imports work
ENV PYTHONPATH=/app

# Default command: run the pipeline
CMD ["python", "main.py"]