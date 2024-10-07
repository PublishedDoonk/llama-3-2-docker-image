from llama_cpp import Llama
from fastapi import FastAPI, HTTPException
import torch
import uvicorn
from pydantic import BaseModel

# Define a request model for validation
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 50

# Initialize the FastAPI app
app = FastAPI()

# Check for CUDA availability
use_cuda = torch.cuda.is_available()

# Initialize Llama model
try:
    model = Llama(model_path="./llama-model/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
                  n_gpu_layers=-1)
    #print("Using CUDA for inference" if use_cuda else "Using CPU for inference")
except Exception as e:
    print("Failed to load model:", e)
    raise e

# Endpoint to generate text based on a given prompt
@app.post("/generate/")
async def generate(request: GenerateRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        return model(prompt=request.prompt, max_tokens=request.max_tokens)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during text generation: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)