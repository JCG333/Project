# Python image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /api_test_runner

ENV PYTHONPATH /api_test_runner

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#  Copies the api-test.py script from the host machine to the container's working directory (api-test-runner)
COPY api_test.py .

# Make the script executable
RUN chmod +x api_test.py

CMD ["Python", "api_test.py"]
