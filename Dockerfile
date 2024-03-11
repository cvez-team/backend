FROM python:3.10.13-slim-bookworm

# Set environment variables
ENV CLOUD_HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Setup new user named user with UID 1000
RUN useradd -m -u 1000 user

# Define working directory
WORKDIR $CLOUD_HOME/app

# Switch to user
USER user

# Copy the requirements file
COPY --chown=user:user requirements.txt /app

# Install the requirements
RUN pip install -r requirements.txt

# Install spacy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the files
COPY --chown=user:user . /app

# Expose the port
EXPOSE 7860/tcp

# Run the application
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]