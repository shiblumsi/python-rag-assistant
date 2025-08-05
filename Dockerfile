FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project code
COPY . .

# Expose port used by Hugging Face Spaces (mandatory)
EXPOSE 7860

# Run FastAPI app located at app/main.py → app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
