"""Stream the answer token by token.

    pip install openai
    export CANONN_API_KEY=...
    python stream.py
"""
import os

from openai import OpenAI

client = OpenAI(base_url="https://api.canonn.ai/v1", api_key=os.environ["CANONN_API_KEY"])

stream = client.chat.completions.create(
    model="canonn-r1",
    stream=True,
    messages=[
        {"role": "system", "content": "Answer from this document.\n\nThe office is open Monday to Friday, 9:00 to 17:30."},
        {"role": "user", "content": "What time does the office close on Friday?"},
    ],
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()
