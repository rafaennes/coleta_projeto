# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python API code
COPY extract_api/ .

# Install Java for PySpark
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Spark
RUN curl -o spark.tgz -L "https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz" && \
    tar -xzf spark.tgz -C /opt/ && \
    rm spark.tgz && \
    mv /opt/spark-3.3.1-bin-hadoop3 /opt/spark

# Add Spark to PATH
ENV PATH="/opt/spark/bin:${PATH}"

# Set the environment variables for PySpark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Command to run the API
CMD ["python", "app.py"]
