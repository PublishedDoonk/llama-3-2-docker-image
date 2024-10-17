# Dockerfile to set up the Llama API project on Ubuntu 22.04
ARG BASE_IMAGE
FROM $BASE_IMAGE

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/lib/x86_64-linux-gnu

# Install Python, pip, ccache, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip cmake build-essential git curl ccache && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a symbolic link for libcuda.so.1 if not already present
#RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/x86_64-linux-gnu/libcuda.so.1

# Run ldconfig to update linker paths
#RUN echo "/usr/local/cuda/lib64" > /etc/ld.so.conf.d/cuda.conf && ldconfig

# Set Python3 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Create a non-root user
RUN useradd -m appuser
USER appuser
ENV PATH=$PATH:/home/appuser/.local/bin

# Set working directory and change ownership to the non-root user
WORKDIR /app

# Download the Llama model from huggingface
RUN mkdir /app/llama-model && \
    curl -L -o /app/llama-model/Llama-3.2-1B-Instruct-Q4_K_M.gguf "https://huggingface.co/lmstudio-community/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf?download=true"

# Copy the FastAPI application files into the container
COPY --chown=appuser . /app

ARG SETUP_SCRIPT
RUN ls -l scripts && \
    echo "Running setup script: $SETUP_SCRIPT" && \
    #chmod +x scripts/$SETUP_SCRIPT && \
    scripts/$SETUP_SCRIPT
#RUN ./scripts/%SETUP_SCRIPT%

# Install Python dependencies and build with CUDA support
#RUN pip install --upgrade pip && \
#    CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda -DCUDA_LIB_DIR=/usr/lib/x86_64-linux-gnu" pip install llama-cpp-python && \
#    #pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121 && \
#    pip install -r requirements.txt

# Remove the symlink to prevent runtime conflicts with NVIDIA runtime
#USER root
#RUN rm /usr/lib/x86_64-linux-gnu/libcuda.so.1

# Switch back to non-root user
#USER appuser

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "llama_cpp_api_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]