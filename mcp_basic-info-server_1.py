from mcp.server.fastmcp import FastMCP

mcp = FastMCP("basic-info-server")

@mcp.tool()
def hello() -> str:
    """
    Simple test tool
    """
    return "Hello from your local MCP server"

if __name__ == "__main__":
    mcp.run()