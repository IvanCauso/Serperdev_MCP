import os
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def serper_post(endpoint: str, payload: dict):
    """Helper to call Serper.dev API."""
    try:
        r = requests.post(
            f"https://google.serper.dev/{endpoint}",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------
# TOOLS (MCP)
# ---------------------------------------------------------

@app.post("/tools/search")
def search_tool(body: dict):
    q = body.get("q")
    num = body.get("num", 10)
    return JSONResponse(serper_post("search", {"q": q, "num": num}))


@app.post("/tools/news")
def news_tool(body: dict):
    q = body.get("q")
    num = body.get("num", 10)
    return JSONResponse(serper_post("news", {"q": q, "num": num}))


@app.post("/tools/images")
def images_tool(body: dict):
    q = body.get("q")
    num = body.get("num", 10)
    return JSONResponse(serper_post("images", {"q": q, "num": num}))


# ---------------------------------------------------------
# MCP MANIFEST
# ---------------------------------------------------------

BASE_URL = os.getenv(
    "PUBLIC_BASE_URL",
    "https://serperdevmcp-production.up.railway.app"
)

MANIFEST = {
    "schema_version": "v1",
    "name_for_human": "Serperdev MCP",
    "name_for_model": "serperdev_mcp",
    "description_for_human": "Google search, news, and image SERP data via Serper.dev.",
    "description_for_model": (
        "Search, news, and images via Serper.dev. "
        "Structured SERP results for AI agents."
    ),
    "auth": {"type": "none"},
    "api": {
        "type": "openapi",
        "url": f"{BASE_URL}/openapi.json"
    },
    "logo_url": "https://serper.dev/favicon.ico",
    "contact_email": "support@serper.dev",
    "legal_info_url": "https://serper.dev/terms",
    "tools": [
        {
            "name": "search",
            "description": "Run a Google search via Serper.dev.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "q": {"type": "string"},
                    "num": {"type": "integer"}
                },
                "required": ["q"]
            }
        },
        {
            "name": "news",
            "description": "Search news articles.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "q": {"type": "string"},
                    "num": {"type": "integer"}
                },
                "required": ["q"]
            }
        },
        {
            "name": "images",
            "description": "Search for images.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "q": {"type": "string"},
                    "num": {"type": "integer"}
                },
                "required": ["q"]
            }
        }
    ]
}


@app.get("/")
def root():
    return {
        "message": "Serperdev MCP is running.",
        "manifest": "/.well-known/ai-plugin.json",
        "health": "/healthz"
    }


@app.get("/healthz")
def health_check():
    return {"ok": True}


@app.get("/.well-known/ai-plugin.json")
@app.get("/.well-known/ai-plugin.json/")
def plugin_manifest():
    return MANIFEST

# IMPORTANT:
# Nixpacks can still launch uvicorn via `python server.py`, so we expose a direct
# entrypoint for Railway and similar environments.

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
