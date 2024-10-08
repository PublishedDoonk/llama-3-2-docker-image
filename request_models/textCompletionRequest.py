from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any

'''
TextCompletionRequest is a Pydantic model that represents a request to the /completions endpoint.
'''
class TextCompletionRequest(BaseModel):
    prompt: Union[str, List[int]]
    suffix: Optional[str] = None
    max_tokens: Optional[int] = 16
    temperature: float = 0.8
    top_p: float = 0.95
    min_p: float = 0.05
    typical_p: float = 1.0
    logprobs: Optional[int] = None
    echo: bool = False
    stop: Optional[Union[str, List[str]]] = ['\n\n']
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    repeat_penalty: float = 1.0
    top_k: int = 40
    stream: bool = False
    seed: Optional[int] = None
    tfs_z: float = 1.0
    mirostat_mode: int = 0
    mirostat_tau: float = 5.0
    mirostat_eta: float = 0.1
    model: Optional[str] = None
    stopping_criteria: Optional[Any] = None
    logits_processor: Optional[Any] = None
    grammar: Optional[Any] = None
    logit_bias: Optional[Dict[str, float]] = None