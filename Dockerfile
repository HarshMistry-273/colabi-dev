FROM python:3.12-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

EXPOSE 8000

CMD ["python", "main.py"]
