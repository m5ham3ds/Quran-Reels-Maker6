import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

def try_url(provider, model):
    url = f"https://router.huggingface.co/{provider}/v1/chat/completions"
    print("Trying:", url)
    try:
        req = urllib.request.Request(url, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", "Bearer hf_test")
        data = json.dumps({"model": model, "messages": [{"role": "user", "content": "hello"}]}).encode("utf-8")
        with urllib.request.urlopen(req, data=data, context=ctx, timeout=5) as response:
            print("Status:", response.status)
    except urllib.error.HTTPError as e:
        print("Error:", e.code, e.read().decode())
    except Exception as e:
        print("Error:", e)

try_url("hf-inference", "Qwen/Qwen2.5-7B-Instruct")
try_url("hf-inference", "meta-llama/Llama-3.1-8B-Instruct")
try_url("together", "Qwen/Qwen2.5-7B-Instruct")
try_url("together", "meta-llama/Llama-3.1-8B-Instruct")
