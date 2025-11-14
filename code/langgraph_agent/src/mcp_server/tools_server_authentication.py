from fastmcp import FastMCP
from fastmcp.server.auth import JWTVerifier
from fastmcp.server.auth.providers.jwt import RSAKeyPair
from fastmcp.server.dependencies import AccessToken, get_access_token

# 1.生成RSA密钥对
key_pair = RSAKeyPair.generate()
# print(key_pair.public_key)
# print(key_pair.private_key)

# 2.签发配置认证提供方
authentication = JWTVerifier(
    public_key=key_pair.public_key, # 公钥用于校验签名
    issuer='https://www.marvelous.com', # 令牌签发方标识
    audience='marvelous_mcp_server', # 服务商的一个标识
)

# 3.服务器，模拟生成一个token
token = key_pair.create_token(
    subject='dev_user',
    issuer='https://www.marvelous.com',
    audience='marvelous_mcp_server',
    scopes=['MarvelousTan','invoke_tools'],
    expires_in_seconds=3600,
)
print(token)

# 签发端就是包含签发配置，并且使用签发配置生成了token,生成token后，token会传给客户端
# 然后客户端发送请求和token给服务端，服务端用对应的签发配置验证token，通过后就可以调用工具


mcp_server = FastMCP(
    name="marvelous_mcp_server",
    instructions="mcp_server made of python",
    auth=authentication, # 服务用于校验token
)

@mcp_server.tool(
    name="say_hello"
)
def say_hello(username: str) -> str:
    """给指定的用户打个招呼"""

    # 得到了验证之后的token
    access_token: AccessToken = get_access_token()
    if access_token:
        print(access_token.scopes)
    else:
        return "token验证失败，没有权限，say_hello工具调用失败"

    return f"Hello, {username}!"

