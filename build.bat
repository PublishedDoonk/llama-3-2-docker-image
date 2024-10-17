@echo off
setlocal

:: Detect if an NVIDIA GPU is present using wmic
wmic path win32_VideoController get name | find /i "NVIDIA" >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo NVIDIA GPU detected. Using CUDA setup script.
    set "SETUP_SCRIPT=cuda_setup.sh"
    set "BASE_IMAGE=nvidia/cuda:12.6.1-devel-ubuntu22.04"
) else (
    echo No NVIDIA GPU detected. Using regular Ubuntu setup script.
    set "SETUP_SCRIPT=cpu_setup.sh"
    set "BASE_IMAGE=ubuntu:20.04"
)

:: Build the Docker image, passing the selected base image and setup script as arguments
docker build --build-arg BASE_IMAGE=%BASE_IMAGE% --build-arg SETUP_SCRIPT=%SETUP_SCRIPT% -t my_app_image .

endlocal
