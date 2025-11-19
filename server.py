import os
import requests
from fastmcp import FastMCP
from typing import Optional, Dict, Any

# Create MCP server
app = FastMCP("serperdev-mcp")

def get_api_key():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SERPER_API_KEY environment variable")
    return api_key

def serper_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    api_key = get_api_key()
    try:
        r = requests.post(
            f"https://google.serper.dev/{endpoint}",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json=params,
            timeout=30
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# TOOLS --------------------------------------------------

@app.tool()
def search(q: str, num: int = 10):
    return serper_request("search", {"q": q, "num": num})

@app.tool()
def images(q: str, num: int = 10):
    return serper_request("images", {"q": q, "num": num})

@app.tool()
def news(q: str, num: int = 10):
    return serper_request("news", {"q": q, "num": num})

@app.tool()
def autocomplete(q: str):
    return serper_request("autocomplete", {"q": q})

# --------------------------------------------------------

# START MCP SERVER ---------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"MCP server running on port {port}")
    app.run(host="0.0.0.0", port=port)
