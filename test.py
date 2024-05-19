from ollama import Client
import httpx

client = Client(host="http://localhost:11434")
try:
    response = client.generate(model="orca-mini", prompt="Hello World!", stream=False)
except httpx.ConnectError:
    print("Failed to connect to Ollama")