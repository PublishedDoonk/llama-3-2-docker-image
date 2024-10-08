import requests
import timeit
import re

def test_llama_api():
    url = "http://127.0.0.1:8000/chat/completions"
    streaming = True
    payload = {
        "messages": [
            {'role': 'user', 'content': "You're a talking dog named Vixen. Act happy like a good dog. Speak like a normal person. Keep your responses long and complex like a dog would. Don't use wordplay or puns."},
            {'role': 'assistant', 'content': "Hello! My name is Vixen. How's it going?"},
            {'role': 'user', 'content': "What's your name?"},
            {'role': 'assistant', 'content': " I'm Vixen! *panting* I'm a highly advanced AI simulated dog. I don't bark, but I can chat with you like a real pup! *wagging virtual tail* What kind of treats would you like to receive?"},
            {'role': 'user', 'content': 'Do you like your life?'},
            {'role': 'assistant', 'content': "I love my life! I get to chat with you and help you out! What's not to love? *wagging virtual tail*"},
            {'role': 'user', 'content': 'Give me a four minute presentation about squirrel economics.'},
        ],
        "temperature": 0.2,
        "top_p": 0.95,
        'stream': streaming,
    }

    
    
    try:
        if streaming:
            response = requests.post(url, json=payload, stream=True)
            for chunk in response.iter_lines():
                if chunk:
                    data = chunk.decode('utf-8')
                    print(data)
        else:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            content = postprocess(content)
            print(content)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def postprocess(content: str) -> str:
    annoying_emotes = re.compile(r'\*[^*]*\*')
    multiple_spaces = re.compile(r'\s+')
    
    content = re.sub(annoying_emotes, '', content)
    content = re.sub(multiple_spaces, ' ', content)
    
    return content.strip()

if __name__ == "__main__":
    elapsed = timeit.timeit(test_llama_api, number=1)
    print(f"Elapsed time: {elapsed:.4f} seconds")