# Step 1: Use a base Python image
FROM python:3.8-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install necessary system dependencies (including ffmpeg and others)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*  # Clean up unnecessary files

# Step 4: Copy the requirements.txt file into the container
COPY requirements.txt .

# Step 5: Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the entire project directory into the container
COPY . .

# Step 7: Define the command to start the bot (assuming your main bot file is bot.py)
CMD ["python", "bot.py"]
