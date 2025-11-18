





# claude联网搜索-mcp服务
python_mcp_claude_search_server_config={
    'url': 'http://localhost:8080/streamable',
    'transport': 'streamable_http',
}

#   "mcpServers": {
#     "12306-mcp": {
#       "type": "streamable_http",
#       "url": "https://mcp.api-inference.modelscope.net/7f92f889f8c94a/mcp"
#     }
#   }

# 12306-mcp服务
python_mcp_12306_server_config={
      "transport": "streamable_http",
      "url": "https://mcp.api-inference.modelscope.net/adeedf98bf8d41/mcp"
}

# {
#   "mcpServers": {
#     "mcp-server-chart": {
#       "type": "streamable_http",
#       "url": "https://mcp.api-inference.modelscope.net/5502466066fc4f/mcp"
#     }
#   }
# }

# 表格制作-mcp服务
python_mcp_table_create_server_config={
      "transport": "streamable_http",
      "url": "https://mcp.api-inference.modelscope.net/d090b73686f942/mcp"
}