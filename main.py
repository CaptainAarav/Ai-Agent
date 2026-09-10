import os
from dotenv import load_dotenv
from openai import OpenAI

# loading the api key from .env
load_dotenv()
api_key: str = os.environ.get("OPENROUTER_API_KEY")

# checks if the api key was found
if api_key is None:
    raise RuntimeError("api key could not be loaded")

user_prompt: str = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

# create a new client that talks to openrouter api
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# creates a new chat completions request with our user prompt
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": user_prompt,
        }
    ],
)

print(f"User prompt: {user_prompt}")
print(f"Model used: {response.model}")
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Response tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Response:\n{response.choices[0].message.content}")