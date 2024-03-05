FROM python:3.11.8-slim-bookworm

# Define working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app

# Install the requirements
RUN pip install -r requirements.txt

# Copy the rest of the files
COPY . /app

# Run the application
ENTRYPOINT ["python", "main.py"]