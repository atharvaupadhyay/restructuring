import os
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="z-ai/glm-5.2",
    messages=[
        {
            "role": "user",
            "content": "Hello! Who are you?"
        }
    ],
    max_tokens=1024
)

print(response.choices[0].message.content)