from langgraph_sdk import get_client
import asyncio

# 调用agent发布的API接口
client = get_client(url="http://localhost:2024")

async def main():
    async for chunk in client.runs.stream(
        None,  # Threadless run
        "agent", # Name of assistant. Defined in langgraph.json.
        input={
        "messages": [{
            "role": "human",
            "content": "给当前用户一个祝福语",
            }],
        },
        # stream_mode="messages-tuple",
        config={"configurable":{"user_name":"Marvelous"}},
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")


asyncio.run(main())