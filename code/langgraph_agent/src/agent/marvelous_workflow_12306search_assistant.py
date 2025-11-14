from langchain_mcp_adapters.client import MultiServerMCPClient

from src.mcp_server.marvelous_mcp_server_config import python_mcp_12306_server_config
from src.mcp_server.marvelous_mcp_server_config import python_mcp_claude_search_server_config
from src.mcp_server.marvelous_mcp_server_config import python_mcp_table_create_server_config

# mcp客户端
mcp_client = MultiServerMCPClient(
    connections={
        "marvelous_claude_search_mcp_server":python_mcp_claude_search_server_config,
        "marvelous_12306_mcp_server": python_mcp_12306_server_config,
        "marvelous_table_create_mcp_server": python_mcp_table_create_server_config,
    }
)