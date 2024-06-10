# Use an official Python runtime as the base image
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

#ENV REDIS_HOST=$REDIS_HOST
#ENV REDIS_PORT=$REDIS_PORT
#ENV CLIENT_ID=$CLIENT_ID
#ENV CLIENT_SECRET=$CLIENT_SECRET
# Set the command to run your application
CMD [ "python", "app.py" ]