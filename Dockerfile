# Use official Python 3.11 base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy only necessary files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining source code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Run the app
CMD ["python", "dashboard/web.py"]
