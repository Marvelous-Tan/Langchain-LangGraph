from src.mcp_server.tools_server_authentication import mcp_server



if __name__ == "__main__":
    mcp_server.run(
        transport="streamable-http",
        host="localhost",
        port=8080,
        log_level="debug",
        path='/streamable',
    )