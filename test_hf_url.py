import os
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
from huggingface_hub import InferenceClient

client = InferenceClient()
print("URL:", client._resolve_url(model="Qwen/Qwen2.5-7B-Instruct", task="chat-completion"))
