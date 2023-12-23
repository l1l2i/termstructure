# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and other utilities
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install requests pandas psycopg2-binary sqlalchemy

# Set the working directory to /app
#WORKDIR /app

# Copy the current directory contents into the container at /app
#COPY . /app

# Run script.py when the container launches
CMD ["python3", "./get_term.py"]