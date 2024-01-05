# Python image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /api-test-runner

ENV PYTHONPATH /api-test-runner

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#  copies the api-test.py script from the host machine to the container's working directory (api-test-runner)
COPY api-test.py .

RUN chmod +x api-test.py

ENTRYPOINT ["python", "api-test.py"]
