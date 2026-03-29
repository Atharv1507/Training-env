# Use an official, lightweight Python image
FROM python:3.11-slim

# Hugging Face Spaces require running as a non-root user for security
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY --chown=user . .

# Expose port 7860 (MANDATORY for Hugging Face Spaces)
EXPOSE 7860

# Command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]