# Use the official Python 3.9 image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run indexer.py first
RUN python main_page_engdb/indexer.py

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["streamlit", "run", "--server.port", "8080", "--server.address", "0.0.0.0", "app.py"]