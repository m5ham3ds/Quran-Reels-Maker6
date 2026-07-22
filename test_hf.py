import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

def try_url(url):
    print("Trying:", url)
    try:
        req = urllib.request.Request(url, method="POST")
        req.add_header("Content-Type", "application/json")
        data = json.dumps({"messages": [{"role": "user", "content": "hello"}]}).encode("utf-8")
        with urllib.request.urlopen(req, data=data, context=ctx, timeout=5) as response:
            print("Status:", response.status)
    except urllib.error.HTTPError as e:
        print("Error:", e.code, e.read().decode())
    except Exception as e:
        print("Error:", e)

try_url("https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct/v1/chat/completions")
try_url("https://router.huggingface.co/hf-inference/models/Qwen/Qwen2.5-7B-Instruct/v1/chat/completions")
try_url("https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct/v1/chat/completions")
try_url("https://router.huggingface.co/hf-inference/models/meta-llama/Llama-3.1-8B-Instruct/v1/chat/completions")
