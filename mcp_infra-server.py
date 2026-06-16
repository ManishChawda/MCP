from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("infra-server")

# -------------------------
# Tool 1 - Hello
# -------------------------
@mcp.tool()
def hello() -> str:
    """
    Test tool
    """
    return "Hello from unified MCP server"

# -------------------------
# Tool 2 - Hostname
# -------------------------
@mcp.tool()
def get_hostname() -> str:
    """
    Get Windows hostname
    """
    result = subprocess.check_output("hostname", shell=True)
    return result.decode().strip()

# -------------------------
# Tool 3 - OS Info
# -------------------------
@mcp.tool()
def get_os_info() -> str:
    """
    Get Windows OS details
    """
    cmd = [
        "powershell",
        "-Command",
        "Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion"
    ]

    result = subprocess.check_output(cmd)
    return result.decode()

# -------------------------
# Tool 4 - IP Address
# -------------------------
@mcp.tool()
def get_ip_address() -> str:
    """
    Get system IP address
    """
    result = subprocess.check_output("ipconfig", shell=True)
    return result.decode()

# -------------------------
# Tool 5 - Logged-in User
# -------------------------
@mcp.tool()
def get_logged_in_user() -> str:
    """
    Get current logged-in user
    """
    result = subprocess.check_output("whoami", shell=True)
    return result.decode().strip()

# -------------------------
# Tool 6 - System Uptime
# -------------------------
@mcp.tool()
def get_uptime() -> str:
    """
    Get system uptime
    """
    cmd = [
        "powershell",
        "-Command",
        "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime"
    ]
    result = subprocess.check_output(cmd)
    return result.decode()


# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    mcp.run()