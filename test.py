import requests
import timeit

def test_llama_api():
    url = "http://127.0.0.1:8000/generate/"
    payload = {
        "prompt": "Tell me something interesting about Paris.",
        "max_tokens": 600
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    elapsed = timeit.timeit(test_llama_api, number=1)
    print(f"Elapsed time: {elapsed:.4f} seconds")