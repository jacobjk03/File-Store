# Use the official Python base image with Python 3.9
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the application files to the container
COPY app.py client.py ./

# Set the entrypoint command to run the Flask server
CMD [ "python", "app.py" ]
