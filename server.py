import os
import requests
from fastmcp import FastMCP
import json

# Server instance
app = FastMCP("Serper MCP")

@app.tool()
def search_google(
    q: str,
    num: int = 10,
    location: str = None,
    gl: str = None,
    hl: str = None,
    autocorrect: bool = True,
    page: int = 1
):
    """Search Google and return structured results.
    
    Args:
        q: Search query (e.g., "CTO of Causo linkedin")
        num: Number of results (default: 10, max: 100)
        location: Location for localized results (e.g., "Austin, Texas, United States")
        gl: Country code for geolocation (e.g., "us", "uk", "de")
        hl: Language code (e.g., "en", "es", "fr")
        autocorrect: Enable autocorrect for typos (default: True)
        page: Page number for pagination (default: 1)
    
    Returns:
        Dictionary containing organic results, knowledge graph, people also ask, related searches
    """
    try:
        print(f"[DEBUG] search_google called: q='{q}', num={num}")
        
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            print("[ERROR] Missing SERPER_API_KEY")
            return {"error": "Missing SERPER_API_KEY environment variable", "results": []}
        
        print(f"[DEBUG] Searching Google for: {q}")
        
        # Build request payload
        payload = {
            "q": q,
            "num": num,
            "autocorrect": autocorrect,
            "page": page
        }
        
        if location:
            payload["location"] = location
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        print(f"[DEBUG] Serper API response status: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        print(f"[DEBUG] Found {len(data.get('organic', []))} organic results")
        
        return {
            "query": q,
            "organic_results": data.get("organic", []),
            "knowledge_graph": data.get("knowledgeGraph"),
            "people_also_ask": data.get("peopleAlsoAsk", []),
            "related_searches": data.get("relatedSearches", []),
            "total_results": len(data.get("organic", []))
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in search_google: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "results": []}


@app.tool()
def search_images(
    q: str,
    num: int = 10,
    location: str = None,
    gl: str = None,
    hl: str = None
):
    """Search Google Images.
    
    Args:
        q: Image search query (e.g., "office workspace")
        num: Number of results (default: 10, max: 100)
        location: Location for localized results
        gl: Country code
        hl: Language code
    
    Returns:
        Dictionary containing image results with URLs, titles, sources, dimensions
    """
    try:
        print(f"[DEBUG] search_images called: q='{q}'")
        
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return {"error": "Missing SERPER_API_KEY environment variable", "images": []}
        
        payload = {"q": q, "num": num}
        if location:
            payload["location"] = location
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        
        response = requests.post(
            "https://google.serper.dev/images",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "query": q,
            "images": data.get("images", []),
            "count": len(data.get("images", []))
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in search_images: {str(e)}")
        return {"error": str(e), "images": []}


@app.tool()
def search_news(
    q: str,
    num: int = 10,
    location: str = None,
    gl: str = None,
    hl: str = None,
    tbs: str = None
):
    """Search Google News.
    
    Args:
        q: News search query (e.g., "AI startups funding")
        num: Number of results (default: 10, max: 100)
        location: Location for localized news
        gl: Country code
        hl: Language code
        tbs: Time filter (e.g., "qdr:h" = past hour, "qdr:d" = past day, "qdr:w" = past week)
    
    Returns:
        Dictionary containing news results with titles, snippets, sources, dates
    """
    try:
        print(f"[DEBUG] search_news called: q='{q}'")
        
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return {"error": "Missing SERPER_API_KEY environment variable", "news": []}
        
        payload = {"q": q, "num": num}
        if location:
            payload["location"] = location
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        if tbs:
            payload["tbs"] = tbs
        
        response = requests.post(
            "https://google.serper.dev/news",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "query": q,
            "news": data.get("news", []),
            "count": len(data.get("news", []))
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in search_news: {str(e)}")
        return {"error": str(e), "news": []}


@app.tool()
def search_places(
    q: str,
    location: str = None,
    gl: str = None,
    hl: str = None
):
    """Search Google Places/Maps.
    
    Args:
        q: Place search query (e.g., "restaurants near me", "hotels in Paris")
        location: Location context (e.g., "New York, NY")
        gl: Country code
        hl: Language code
    
    Returns:
        Dictionary containing places with ratings, addresses, phone numbers, GPS coordinates
    """
    try:
        print(f"[DEBUG] search_places called: q='{q}'")
        
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return {"error": "Missing SERPER_API_KEY environment variable", "places": []}
        
        payload = {"q": q}
        if location:
            payload["location"] = location
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        
        response = requests.post(
            "https://google.serper.dev/places",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "query": q,
            "places": data.get("places", []),
            "count": len(data.get("places", []))
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in search_places: {str(e)}")
        return {"error": str(e), "places": []}


@app.tool()
def search_shopping(
    q: str,
    num: int = 10,
    location: str = None,
    gl: str = None,
    hl: str = None
):
    """Search Google Shopping.
    
    Args:
        q: Product search query (e.g., "Nike Air Max", "iPhone 15")
        num: Number of results (default: 10)
        location: Location for price localization
        gl: Country code
        hl: Language code
    
    Returns:
        Dictionary containing products with prices, ratings, sellers, availability
    """
    try:
        print(f"[DEBUG] search_shopping called: q='{q}'")
        
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return {"error": "Missing SERPER_API_KEY environment variable", "shopping": []}
        
        payload = {"q": q, "num": num}
        if location:
            payload["location"] = location
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        
        response = requests.post(
            "https://google.serper.dev/shopping",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "query": q,
            "shopping": data.get("shopping", []),
            "count": len(data.get("shopping", []))
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in search_shopping: {str(e)}")
        return {"error": str(e), "shopping": []}


@app.tool()
def search_videos(
    q: str,
    num: int = 10,
    location: str = None,
    gl: str = None,
    hl: str = None
):
    """Search Google Videos.
    
    Args:
        q: Video search query
        num: Number of results (default: 10)
        location: Location for localized results
        gl: Country code
        hl: Language code
    
    Returns:
        Dictionary containing video results with titles, channels, durations, thumbnails
    """
    try:
        print(f"[DEBUG] search_videos called: q='{q}'")
        
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return {"error": "Missing SERPER_API_KEY environment variable", "videos": []}
        
        payload = {"q": q, "num": num}
        if location:
            payload["location"] = location
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        
        response = requests.post(
            "https://google.serper.dev/videos",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "query": q,
            "videos": data.get("videos", []),
            "count": len(data.get("videos", []))
        }
        
    except Exception as e:
        print(f"[ERROR] Exception in search_videos: {str(e)}")
        return {"error": str(e), "videos": []}


@app.tool()
def get_search_info():
    """Get information about available Serper search types and features.
    
    Returns:
        Dictionary with available search types and usage information
    """
    return {
        "search_types": [
            {
                "name": "search_google",
                "description": "General web search - Returns organic results, knowledge graph, people also ask"
            },
            {
                "name": "search_images",
                "description": "Image search - Returns images with URLs, dimensions, sources"
            },
            {
                "name": "search_news",
                "description": "News search - Returns news articles with dates, sources, time filters"
            },
            {
                "name": "search_places",
                "description": "Local businesses/maps - Returns places with ratings, addresses, GPS"
            },
            {
                "name": "search_shopping",
                "description": "Product search - Returns products with prices, ratings, sellers"
            },
            {
                "name": "search_videos",
                "description": "Video search - Returns videos with titles, channels, durations"
            }
        ],
        "features": {
            "geotargeting": "Use 'location' or 'gl' parameters for localized results",
            "languages": "Use 'hl' parameter for different languages (e.g., 'en', 'es', 'fr')",
            "time_filters": "Use 'tbs' parameter for news (e.g., 'qdr:d' for past day)",
            "pagination": "Use 'num' (up to 100) and 'page' parameters"
        },
        "cost": "$0.002 per search",
        "note": "All searches return structured JSON data"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    api_key = os.getenv("SERPER_API_KEY")
    if api_key:
        print(f"[INFO] ✓ SERPER_API_KEY is set")
    else:
        print(f"[WARNING] ✗ SERPER_API_KEY is NOT set - all searches will fail")
    
    print(f"[INFO] Starting Serper MCP server on port {port}")
    # Run with HTTP transport for MCP
    app.run("http", host="0.0.0.0", port=port)