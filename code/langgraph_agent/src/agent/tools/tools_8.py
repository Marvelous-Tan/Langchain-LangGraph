import anthropic

client = anthropic.Anthropic(api_key="sk-W4xyJa17yfll5gFXNrYDvIaOrcr4dJJyu3GNA2sI1usWgBWK",
            base_url="https://globalai.vip",)

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": "What's the weather in NYC?"
        }
    ],
    tools=[{
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5
    }]
)
print(response)
print(next((b.text for b in reversed(response.content) if b.type == "text"), ""))
