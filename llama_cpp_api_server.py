from llama_cpp import Llama
from fastapi import FastAPI, HTTPException
import torch
import uvicorn
from typing import List, Optional, Union, Dict, Any
from request_models import ChatCompletionRequest, TextCompletionRequest
from fastapi.responses import StreamingResponse


# Initialize the FastAPI app
app = FastAPI()

# Check for CUDA availability
n_gpu_layers = -int(torch.cuda.is_available())


# Initialize Llama model
try:
    model = Llama(model_path="./llama-model/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
                  n_gpu_layers=n_gpu_layers,
                  n_ctx=8192,
                  n_batch=2048,
                  n_ubatch=2048,
                  flash_attn=True,)
    #print("Using CUDA for inference" if use_cuda else "Using CPU for inference")
except Exception as e:
    print("Failed to load model:", e)
    raise e

# Endpoint to generate text based on a given prompt
@app.post("/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="Must provide 'messages' argument to generate a meaningful chat response.")
    try:
        args: dict = request.dict()
        
        if not request.stream:
            return model.create_chat_completion(**args)
        
        async def event_stream():
            for chunk in model.create_chat_completion(**args):
                yield chunk['choices'][0]['delta'].get('content', '')
                               
        return StreamingResponse(event_stream(), media_type='text/plain')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat generation: {e}")

@app.post("/completions")
async def create_text_completion(request: TextCompletionRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        args: dict = request.dict()
        return model(**args)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during text generation: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)