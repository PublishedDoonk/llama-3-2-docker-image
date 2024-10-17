#!/bin/bash

# Install Python dependencies
echo "Upgrading pip..."
pip install --upgrade pip

echo "Building llama.cpp with CPU only..."
# Build without CUDA support
pip install llama-cpp-python

echo "Installing additional requirements..."
pip install -r requirements.txt
