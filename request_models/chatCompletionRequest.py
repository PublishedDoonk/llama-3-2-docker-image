from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any

'''
ChatCompletionRequest is a Pydantic model that represents a request to the chat/completions endpoint.
'''
class ChatCompletionRequest(BaseModel):
    messages: List[Dict]  # [{'role': 'system | user | assistant', 'content': str}]
    functions: Optional[List[Dict]] = None  # [{'name': str, 'description': NotRequired[str], 'parameters': Dict[str, JsonType]}]
    function_call: Optional[Any] = None  # Union[Literal["none", "auto"], {'name': str}]
    tools: Optional[List[Dict]] = None  # [{'type': Literal["function"], 'function': {'name': str, 'arguments': str}}]
    tool_choice: Optional[Any] = None  # Union[Literal["none", "auto", "required"], {'type': Literal["function"], 'function': {'name': str}}]
    temperature: float = 0.2
    top_p: float = 0.95
    top_k: int = 40
    min_p: float = 0.05
    typical_p: float = 1.0
    stream: bool = False
    stop: Optional[Union[str, List[str]]] = []
    seed: Optional[int] = None
    response_format: Optional[Any] = None
    max_tokens: Optional[int] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    tfs_z: float = 1.0
    mirostat_mode: int = 0
    mirostat_tau: float = 5.0
    mirostat_eta: float = 0.1
    model: Optional[str] = None
    logits_processor: Optional[Any] = None
    grammar: Optional[Any] = None
    logit_bias: Optional[Dict[str, float]] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None