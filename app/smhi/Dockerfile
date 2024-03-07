# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Set the PYTHONPATH environment variable
ENV PYTHONPATH /app
ENV IMAGE_URL /home/upload/ftp/data/raw_data/2023

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Print the contents of the active directory
RUN ls

# Make port 80 available to the world outside this container
EXPOSE 80

# Run smhi_data_fetch.py when the container launches
CMD ["python", "smhi/listener_files_and_weather.py"]
