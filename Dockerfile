# Dockerfile to set up the Llama API project on Ubuntu 22.04

# Start from the official Ubuntu 22.04 base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip cmake build-essential git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python3 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Create a working directory
WORKDIR /app

# Download the Llama model from huggingface
RUN mkdir /app/llama-model && \
    curl -L -o /app/llama-model/Llama-3.2-1B-Instruct-Q4_K_M.gguf "https://huggingface.co/lmstudio-community/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf?download=true"

# Copy the FastAPI application files into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "llama_cpp_api_server:app", "--host", "0.0.0.0", "--port", "8000"]