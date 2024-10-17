#!/bin/bash

# Install Python dependencies
echo "Upgrading pip..."
pip install --upgrade pip

# Build with CUDA support
ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/x86_64-linux-gnu/libcuda.so.1
echo "Building with CUDA support..."
echo "/usr/local/cuda/lib64" > /etc/ld.so.conf.d/cuda.conf && ldconfig
CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda -DCUDA_LIB_DIR=/usr/lib/x86_64-linux-gnu" pip install llama-cpp-python


# Install python requirements
echo "Installing additional requirements..."
pip install -r requirements.txt

echo "Cleaning up conflicting CUDA symlinks..."
# Remove the symlink to prevent runtime conflicts with NVIDIA runtime
rm /usr/lib/x86_64-linux-gnu/libcuda.so.1 || true
