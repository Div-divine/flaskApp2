# Base image
FROM python:3.9.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required dependencies
# Install the required dependencies using the second virtual environment
RUN pip install -r requirements.txt 
# Copy the entire project directory to the working directory
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
