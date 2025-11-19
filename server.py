import os
import requests
from fastmcp import FastMCP
from typing import Optional, List, Dict, Any

app = FastMCP("Serper Complete MCP")

def get_api_key():
    """Get Serper API key from environment"""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SERPER_API_KEY environment variable")
    return api_key


def serper_request(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Make a request to Serper API"""
    api_key = get_api_key()
    
    try:
        response = requests.post(
            f"https://google.serper.dev/{endpoint}",
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Serper {endpoint} failed: {str(e)}")
        return {"error": str(e)}


@app.tool()
def search(
    q: str,
    num: int = 10,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
    autocorrect: bool = True,
    page: int = 1
):
    """Google Web Search - Main search functionality.
    
    Args:
        q: Search query (required)
        num: Number of results (default: 10, max: 100)
        location: Location for localized results (e.g., "Austin, Texas, United States")
        gl: Country code for geolocation (e.g., "us", "uk", "de")
        hl: Language code (e.g., "en", "es", "fr")
        autocorrect: Enable autocorrect for typos (default: True)
        page: Page number for pagination (default: 1)
    
    Returns:
        Organic results, knowledge graph, people also ask, related searches, etc.
    """
    print(f"[DEBUG] Web Search: {q}")
    
    params = {"q": q, "num": num, "autocorrect": autocorrect, "page": page}
    if location:
        params["location"] = location
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    
    return serper_request("search", params)


@app.tool()
def images(
    q: str,
    num: int = 10,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
    autocorrect: bool = True
):
    """Google Images Search - Search for images.
    
    Args:
        q: Search query (required)
        num: Number of results (default: 10, max: 100)
        location: Location for localized results
        gl: Country code for geolocation
        hl: Language code
        autocorrect: Enable autocorrect (default: True)
    
    Returns:
        Image results with URLs, titles, sources, dimensions
    """
    print(f"[DEBUG] Image Search: {q}")
    
    params = {"q": q, "num": num, "autocorrect": autocorrect}
    if location:
        params["location"] = location
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    
    return serper_request("images", params)


@app.tool()
def news(
    q: str,
    num: int = 10,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
    tbs: Optional[str] = None,
    autocorrect: bool = True
):
    """Google News Search - Search for news articles.
    
    Args:
        q: Search query (required)
        num: Number of results (default: 10, max: 100)
        location: Location for localized news
        gl: Country code
        hl: Language code
        tbs: Time-based search (e.g., "qdr:h" = past hour, "qdr:d" = past day, "qdr:w" = past week)
        autocorrect: Enable autocorrect (default: True)
    
    Returns:
        News results with titles, snippets, sources, dates, image URLs
    """
    print(f"[DEBUG] News Search: {q}")
    
    params = {"q": q, "num": num, "autocorrect": autocorrect}
    if location:
        params["location"] = location
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    if tbs:
        params["tbs"] = tbs
    
    return serper_request("news", params)


@app.tool()
def places(
    q: str,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None
):
    """Google Places/Maps Search - Search for local businesses and places.
    
    Args:
        q: Search query (e.g., "restaurants near me", "hotels in Paris")
        location: Location context (e.g., "New York, NY")
        gl: Country code
        hl: Language code
    
    Returns:
        Places with ratings, addresses, phone numbers, hours, GPS coordinates
    """
    print(f"[DEBUG] Places Search: {q}")
    
    params = {"q": q}
    if location:
        params["location"] = location
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    
    return serper_request("places", params)


@app.tool()
def shopping(
    q: str,
    num: int = 10,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
    tbs: Optional[str] = None
):
    """Google Shopping Search - Search for products and prices.
    
    Args:
        q: Product search query (e.g., "Nike Air Max", "iPhone 15")
        num: Number of results (default: 10)
        location: Location for price localization
        gl: Country code
        hl: Language code
        tbs: Filters (e.g., "mr:1,price:1,ppr_min:100,ppr_max:500" for price range)
    
    Returns:
        Products with prices, ratings, sellers, availability, images
    """
    print(f"[DEBUG] Shopping Search: {q}")
    
    params = {"q": q, "num": num}
    if location:
        params["location"] = location
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    if tbs:
        params["tbs"] = tbs
    
    return serper_request("shopping", params)


@app.tool()
def videos(
    q: str,
    num: int = 10,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
    autocorrect: bool = True
):
    """Google Videos Search - Search for video content.
    
    Args:
        q: Search query (required)
        num: Number of results (default: 10)
        location: Location for localized results
        gl: Country code
        hl: Language code
        autocorrect: Enable autocorrect (default: True)
    
    Returns:
        Video results with titles, channels, durations, thumbnails, links
    """
    print(f"[DEBUG] Video Search: {q}")
    
    params = {"q": q, "num": num, "autocorrect": autocorrect}
    if location:
        params["location"] = location
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    
    return serper_request("videos", params)


@app.tool()
def scholar(
    q: str,
    num: int = 10,
    hl: Optional[str] = None
):
    """Google Scholar Search - Search for academic papers and citations.
    
    Args:
        q: Academic search query (e.g., "machine learning transformers")
        num: Number of results (default: 10)
        hl: Language code
    
    Returns:
        Academic papers with titles, authors, citations, publication info, PDF links
    """
    print(f"[DEBUG] Scholar Search: {q}")
    
    params = {"q": q, "num": num}
    if hl:
        params["hl"] = hl
    
    return serper_request("scholar", params)


@app.tool()
def patents(
    q: str,
    num: int = 10,
    hl: Optional[str] = None
):
    """Google Patents Search - Search for patents.
    
    Args:
        q: Patent search query (e.g., "machine learning classification")
        num: Number of results (default: 10)
        hl: Language code
    
    Returns:
        Patents with titles, inventors, assignees, dates, descriptions, PDFs
    """
    print(f"[DEBUG] Patents Search: {q}")
    
    params = {"q": q, "num": num}
    if hl:
        params["hl"] = hl
    
    return serper_request("patents", params)


@app.tool()
def autocomplete(
    q: str,
    gl: Optional[str] = None,
    hl: Optional[str] = None
):
    """Google Autocomplete - Get search suggestions.
    
    Args:
        q: Partial search query (e.g., "how to")
        gl: Country code
        hl: Language code
    
    Returns:
        List of autocomplete suggestions
    """
    print(f"[DEBUG] Autocomplete: {q}")
    
    params = {"q": q}
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    
    return serper_request("autocomplete", params)


@app.tool()
def trends(
    q: str,
    location: Optional[str] = None
):
    """Google Trends - Get trending searches and interest over time.
    
    Args:
        q: Search term to get trends for
        location: Location for localized trends
    
    Returns:
        Trend data including interest over time, related queries
    """
    print(f"[DEBUG] Trends: {q}")
    
    params = {"q": q}
    if location:
        params["location"] = location
    
    return serper_request("trends", params)


@app.tool()
def get_supported_locations():
    """Get list of supported locations for geotargeting.
    
    Returns:
        Dictionary of supported countries and location formats
    """
    return {
        "countries": {
            "us": "United States",
            "uk": "United Kingdom",
            "ca": "Canada",
            "au": "Australia",
            "de": "Germany",
            "fr": "France",
            "es": "Spain",
            "it": "Italy",
            "nl": "Netherlands",
            "br": "Brazil",
            "mx": "Mexico",
            "in": "India",
            "jp": "Japan",
            "cn": "China"
        },
        "location_format": "City, State, Country (e.g., 'Austin, Texas, United States')",
        "note": "Use 'location' parameter for specific cities or 'gl' for country-level results"
    }


@app.tool()
def get_supported_languages():
    """Get list of supported language codes.
    
    Returns:
        Dictionary of language codes and their meanings
    """
    return {
        "languages": {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
            "ar": "Arabic",
            "hi": "Hindi",
            "nl": "Dutch",
            "pl": "Polish",
            "tr": "Turkish"
        },
        "usage": "Use 'hl' parameter (e.g., hl='es' for Spanish results)"
    }


@app.tool()
def get_time_filters():
    """Get available time-based search filters.
    
    Returns:
        Dictionary of time filter options for news and search
    """
    return {
        "tbs_options": {
            "qdr:h": "Past hour",
            "qdr:d": "Past 24 hours",
            "qdr:w": "Past week",
            "qdr:m": "Past month",
            "qdr:y": "Past year"
        },
        "usage": "Use 'tbs' parameter (e.g., tbs='qdr:d' for past day)",
        "applicable_to": ["news", "search", "shopping"]
    }


@app.tool()
def get_api_info():
    """Get information about Serper API capabilities and costs.
    
    Returns:
        API information, features, and credit costs
    """
    return {
        "endpoints": {
            "search": "General web search",
            "images": "Image search",
            "news": "News articles",
            "places": "Local businesses/maps",
            "shopping": "Product search",
            "videos": "Video search",
            "scholar": "Academic papers",
            "patents": "Patent search",
            "autocomplete": "Search suggestions",
            "trends": "Trending searches"
        },
        "features": {
            "speed": "1-2 second response time",
            "geotargeting": "50+ countries supported",
            "languages": "25+ languages",
            "pagination": "Up to 100 results per query",
            "autocorrect": "Automatic typo correction",
            "real_time": "No caching, always fresh results"
        },
        "pricing": {
            "free_tier": "2,500 queries",
            "cost_per_query": "$0.002 (after free tier)",
            "rate_limit": "300 queries per second (Ultimate tier)"
        },
        "response_format": "Structured JSON with parsed data"
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    api_key = os.getenv("SERPER_API_KEY")
    
    if api_key:
        print(f"[INFO] ✓ SERPER_API_KEY is set")
    else:
        print(f"[WARNING] ✗ SERPER_API_KEY is NOT set")
    
    print(f"[INFO] Starting Serper Complete MCP on port {port}")
    print(f"[INFO] Available endpoints: search, images, news, places, shopping, videos, scholar, patents, autocomplete, trends")
    print(f"[INFO] Cost: $0.002 per search (~$2 for 1,000 searches)")
    
    app.run("http", host="0.0.0.0", port=port)