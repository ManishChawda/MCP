from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("basic-info-server")

@mcp.tool()
def get_hostname() -> str:
    """
    Get Windows hostname
    """
    result = subprocess.check_output("hostname", shell=True)
    return result.decode().strip()

if __name__ == "__main__":
    mcp.run()