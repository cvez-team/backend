FROM python:3.11.8-slim-bookworm

# Define working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app

# Install the requirements
RUN pip install -r requirements.txt

# Install spacy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the files
COPY . /app

# Expose the port
EXPOSE 7860

# Run the application
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]