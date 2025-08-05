# Use official Python image
FROM python:3.9

# Create and switch to a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY --chown=user ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app code
COPY --chown=user . .

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
