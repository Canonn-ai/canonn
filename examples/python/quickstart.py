"""Ask Canonn R1 a question about your own document.

    pip install openai
    export CANONN_API_KEY=...   # https://canonn.ai/dashboard/
    python quickstart.py
"""
import os

from openai import OpenAI

client = OpenAI(base_url="https://api.canonn.ai/v1", api_key=os.environ["CANONN_API_KEY"])

document = """Northwind returns policy.
Returns are accepted within 30 days of delivery.
Refunds go back to the original payment method within 5 business days."""

reply = client.chat.completions.create(
    model="canonn-r1",
    messages=[
        {"role": "system", "content": "Answer from this document.\n\n" + document},
        {"role": "user", "content": "How long do refunds take?"},
    ],
)
print(reply.choices[0].message.content)
