from src.mcp_server.tools_server import mcp_server



if __name__ == "__main__":
    mcp_server.run(
        transport="sse",
        host="localhost",
        port=8080,
        log_level="debug",
        path='/sse',
    )