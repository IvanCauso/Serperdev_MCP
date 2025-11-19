import os
import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


SERPER_API_KEY = os.getenv("SERPER_API_KEY")


class QueryPayload(BaseModel):
    q: str = Field(..., description="Search query text.")
    num: int = Field(
        10,
        ge=1,
        le=20,
        description="Number of results to return from Serper.",
    )


def serper_post(endpoint: str, payload: dict):
    """Helper to call Serper.dev API."""
    if not SERPER_API_KEY:
        return {"error": "SERPER_API_KEY is not configured"}

    try:
        r = requests.post(
            f"https://google.serper.dev/{endpoint}",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


port = int(os.getenv("PORT", "8080"))

app = FastMCP(
    "Serperdev MCP",
    instructions="Google SERP, news, and image results via Serper.dev",
    host="0.0.0.0",
    port=port,
)


@app.tool()
def search(payload: QueryPayload):
    """Run a Google search via Serper.dev."""
    return serper_post("search", payload.model_dump())


@app.tool()
def news(payload: QueryPayload):
    """Search news articles via Serper.dev."""
    return serper_post("news", payload.model_dump())


@app.tool()
def images(payload: QueryPayload):
    """Search for images via Serper.dev."""
    return serper_post("images", payload.model_dump())


if __name__ == "__main__":
    app.run("streamable-http")
