from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

mcp = FastMCP("sophos-server")

# 🔐 Replace with your actual values
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# 🔹 Get Access Token
def get_access_token():
    url = "https://id.sophos.com/api/v2/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "CLIENT_ID": CLIENT_ID,
        "CLIENT_SECRET": CLIENT_SECRET,
        "scope": "token"
    }

    response = requests.post(url, data=data)
    return response.json()["access_token"]


# 🔹 Get Tenant + Region
def get_tenant_and_region(token):
    url = "https://api.central.sophos.com/whoami/v1"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()


# 🔹 TOOL 1 — Get Firewalls (with optional filtering)
@mcp.tool()
def get_firewalls(location: str = "") -> str:
    """
    Get Sophos firewalls.

    You can ask:
    - show all firewalls
    - show MCP firewall
    - show GRKL firewall
    """

    token = get_access_token()
    info = get_tenant_and_region(token)

    tenant_id = info["id"]
    api_host = info["apiHosts"]["dataRegion"]

    url = f"{api_host}/firewall/v1/firewalls"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": tenant_id
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    result = []

    for fw in data.get("items", []):
        name = fw.get("hostname", "N/A")
        model = fw.get("model", "N/A")
        ip = fw.get("externalIpv4Addresses", [])
        status = fw.get("status", {}).get("connected", False)

        line = f"{name} | {model} | IP: {ip} | Online: {status}"

        # 🔥 Filter if location provided
        if location:
            if location.lower() in name.lower():
                result.append(line)
        else:
            result.append(line)

    return "\n".join(result) if result else "No firewalls found."


# 🔹 TOOL 2 — Firewall Summary
@mcp.tool()
def firewall_summary() -> str:
    """
    Get summary of all firewalls (total count and online status)
    """

    token = get_access_token()
    info = get_tenant_and_region(token)

    tenant_id = info["id"]
    api_host = info["apiHosts"]["dataRegion"]

    url = f"{api_host}/firewall/v1/firewalls"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": tenant_id
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    items = data.get("items", [])

    total = len(items)
    online = sum(1 for fw in items if fw.get("status", {}).get("connected"))

    return f"Total Firewalls: {total}, Online: {online}"


# 🔹 Run MCP Server
if __name__ == "__main__":
    mcp.run()
