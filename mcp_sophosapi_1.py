from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

mcp = FastMCP("sophos-server")

# 🔐 Your credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


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


def get_tenant_and_region(token):
    url = "https://api.central.sophos.com/whoami/v1"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()


@mcp.tool()
def get_firewalls(location: str = "") -> str:
    """
    Get Sophos firewalls.
    Optionally filter by location like MCP or GRKL.
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
        name = fw.get("hostname")
        model = fw.get("model")
        ip = fw.get("externalIpv4Addresses", [])
        status = fw.get("status", {}).get("connected")

        line = f"{name} | {model} | IP: {ip} | Online: {status}"

        # 🔥 Filter logic (optional)
        if location:
            if location.lower() in name.lower():
                result.append(line)
        else:
            result.append(line)

    return "\n".join(result)


if __name__ == "__main__":
    mcp.run()