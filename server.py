import os
import requests
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

@app.get("/.well-known/ai-plugin.json")
def plugin_manifest():
    return {
        "schema_version": "v1",
        "name_for_human": "Serperdev MCP",
        "name_for_model": "serperdev_mcp",
        "description_for_model": (
            "Search, news, and images via Serper.dev. "
            "Structured SERP results for AI agents."
        ),
        "auth": {"type": "none"},
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

# IMPORTANT:
# Do NOT run uvicorn here. The process is launched by Nixpacks (see nixpacks.toml).
