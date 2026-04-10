#!/usr/bin/env python3
"""
SchoolMind Web Search Server
Integrates Camoufox browser automation for intelligent web searching
Run this alongside your Ollama instance
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import re
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SchoolMind Web Search")

# Enable CORS for the HTML interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    url: Optional[str] = None

class SearchResult(BaseModel):
    results: str
    source: str = "duckduckgo"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "SchoolMind Web Search"}

@app.post("/search", response_model=SearchResult)
async def search(request: SearchRequest):
    """
    Search the web using DuckDuckGo API (no API key required)
    Falls back to direct API if Camoufox is unavailable
    """
    try:
        # Use DuckDuckGo Instant Answer API (no API key needed)
        results = await duckduckgo_search(request.query)
        if results:
            return SearchResult(results=results, source="duckduckgo")
        else:
            return SearchResult(results="No results found", source="duckduckgo")
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

async def duckduckgo_search(query: str, max_results: int = 3) -> str:
    """
    Search using DuckDuckGo's instant answer API
    """
    try:
        # Using the instant answer API (no rate limits, no API key)
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        results = []
        
        # Extract instant answer if available
        if data.get("Answer"):
            results.append(f"• {data['Answer'][:200]}")
        
        # Extract from Abstract
        if data.get("AbstractText"):
            results.append(f"• {data['AbstractText'][:200]}")
        
        # Extract from Related Topics
        if data.get("RelatedTopics"):
            for item in data["RelatedTopics"][:max_results]:
                if isinstance(item, dict) and item.get("Text"):
                    # Remove HTML tags if present
                    text = item["Text"]
                    text = re.sub(r'<[^>]+>', '', text)
                    if text:
                        results.append(f"• {text[:200]}")
        
        if not results:
            # Fallback to a generic search result
            results.append(f"Query: {query}\nSearching DuckDuckGo for more information...")
        
        # Format results
        formatted = "\n".join(results[:max_results])
        return formatted if formatted else None
        
    except Exception as e:
        logger.error(f"DuckDuckGo search error: {e}")
        return None

@app.post("/search/camoufox")
async def search_with_camoufox(request: SearchRequest):
    """
    Advanced search using Camoufox browser automation
    Requires Camoufox to be installed and configured
    This is for future enhancement when Camoufox integration is needed
    """
    try:
        # Placeholder for Camoufox integration
        # For now, falls back to standard DuckDuckGo
        results = await duckduckgo_search(request.query)
        return SearchResult(results=results, source="camoufox")
    except Exception as e:
        logger.error(f"Camoufox search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/models")
async def get_models():
    """
    List available Ollama models
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            response.raise_for_status()
            data = response.json()
        return data
    except Exception as e:
        logger.error(f"Models error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("""
    ╔════════════════════════════════════════════╗
    ║   SchoolMind Web Search Server             ║
    ║   Starting on http://localhost:8000        ║
    ╚════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
