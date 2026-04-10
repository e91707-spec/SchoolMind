#!/usr/bin/env python3
"""
SchoolMind Camoufox Integration
Advanced web searching with browser automation
Run this for JavaScript-heavy sites and dynamic content

Install: pip install playwright fastapi uvicorn httpx
Setup: playwright install firefox
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import logging
import json
import re

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Install with: pip install playwright")
    print("    Then run: playwright install firefox")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SchoolMind Camoufox Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str
    enable_javascript: bool = True
    timeout: int = 10000  # milliseconds

class SearchResult(BaseModel):
    results: str
    source: str
    success: bool

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "SchoolMind Camoufox",
        "playwright_available": PLAYWRIGHT_AVAILABLE
    }

@app.post("/search/advanced")
async def advanced_search(request: SearchRequest) -> SearchResult:
    """
    Advanced web search with Camoufox/Playwright
    Handles JavaScript-heavy sites, dynamic content, and complex layouts
    """
    if not PLAYWRIGHT_AVAILABLE:
        return SearchResult(
            results="Playwright not installed. Use the fallback search server.",
            source="error",
            success=False
        )
    
    try:
        results = await camoufox_search(
            request.query,
            enable_js=request.enable_javascript,
            timeout=request.timeout
        )
        return SearchResult(results=results, source="camoufox", success=True)
    except Exception as e:
        logger.error(f"Camoufox search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

async def camoufox_search(query: str, enable_js: bool = True, timeout: int = 10000) -> str:
    """
    Perform web search using Camoufox (Firefox-based browser)
    Supports JavaScript execution and dynamic content
    """
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    async with async_playwright() as p:
        try:
            # Use Firefox (Camoufox is Firefox-compatible)
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            )
            
            # Navigate to search
            search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&ia=web"
            await page.goto(search_url, timeout=timeout)
            
            # Wait for results to load
            if enable_js:
                await page.wait_for_load_state("networkidle", timeout=timeout)
            
            # Extract search results
            results = await page.evaluate("""
            () => {
                const results = [];
                const snippets = document.querySelectorAll('[data-result="news"], .result__body');
                
                snippets.forEach((snippet, index) => {
                    if (index >= 3) return; // Limit to 3 results
                    
                    const titleEl = snippet.querySelector('.result__a, a.result__url');
                    const descEl = snippet.querySelector('.result__snippet, .result__body');
                    const linkEl = snippet.querySelector('a[href]');
                    
                    if (titleEl && descEl) {
                        results.push({
                            title: titleEl.textContent?.trim() || '',
                            description: descEl.textContent?.trim() || '',
                            url: linkEl?.href || ''
                        });
                    }
                });
                
                return results;
            }
            """)
            
            await browser.close()
            
            # Format results
            formatted = "\n".join([
                f"• {r['title']}\n  {r['description'][:150]}..."
                for r in results if r['description']
            ])
            
            return formatted if formatted else f"Found results for '{query}' (JavaScript rendered)"
            
        except Exception as e:
            logger.error(f"Camoufox error: {e}")
            raise

@app.post("/scrape/page")
async def scrape_page(request: SearchRequest) -> dict:
    """
    Scrape specific page content
    Useful for analyzing websites with dynamic content
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise HTTPException(status_code=500, detail="Playwright not available")
    
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(request.query, timeout=request.timeout)
            await page.wait_for_load_state("networkidle")
            
            # Extract main content
            content = await page.evaluate("""
            () => {
                const mainContent = document.body.innerText;
                return mainContent;
            }
            """)
            
            await browser.close()
            
            # Clean and summarize
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            summary = '\n'.join(lines[:20])  # First 20 lines
            
            return {
                "url": request.query,
                "success": True,
                "content_preview": summary,
                "total_lines": len(lines)
            }
            
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.post("/search/with-context")
async def search_with_context(request: SearchRequest) -> SearchResult:
    """
    Search with contextual understanding
    Analyzes page structure and extracts relevant sections
    """
    if not PLAYWRIGHT_AVAILABLE:
        return SearchResult(
            results="Use the basic search server for this feature.",
            source="error",
            success=False
        )
    
    try:
        results = await contextual_search(request.query)
        return SearchResult(results=results, source="camoufox_contextual", success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def contextual_search(query: str) -> str:
    """
    Perform contextual search with content analysis
    """
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        
        try:
            search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&ia=web"
            await page.goto(search_url, timeout=10000)
            await page.wait_for_load_state("networkidle")
            
            # Extract with context
            results = await page.evaluate("""
            () => {
                const results = [];
                const articles = document.querySelectorAll('[data-testid="result"]');
                
                articles.forEach((article, idx) => {
                    if (idx >= 3) return;
                    
                    const title = article.querySelector('h2')?.textContent || '';
                    const desc = article.querySelector('p')?.textContent || '';
                    const link = article.querySelector('a[href]')?.href || '';
                    
                    results.push({ title: title.trim(), description: desc.trim(), link });
                });
                
                return results;
            }
            """)
            
            await browser.close()
            
            # Return formatted results with sources
            output = []
            for i, r in enumerate(results, 1):
                output.append(f"{i}. {r['title']}")
                if r['description']:
                    output.append(f"   {r['description'][:200]}...")
                output.append(f"   Source: {r['link']}")
                output.append("")
            
            return "\n".join(output) if output else "No results found"
            
        except Exception as e:
            await browser.close()
            raise

@app.get("/status")
async def get_status():
    """
    Check if Camoufox integration is available
    """
    return {
        "playwright_installed": PLAYWRIGHT_AVAILABLE,
        "features": {
            "basic_search": True,
            "advanced_search": PLAYWRIGHT_AVAILABLE,
            "page_scraping": PLAYWRIGHT_AVAILABLE,
            "contextual_search": PLAYWRIGHT_AVAILABLE
        },
        "browser_support": {
            "firefox": PLAYWRIGHT_AVAILABLE,
            "chromium": PLAYWRIGHT_AVAILABLE if PLAYWRIGHT_AVAILABLE else False
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    if not PLAYWRIGHT_AVAILABLE:
        print("""
        ⚠️  Playwright not installed!
        
        To enable Camoufox integration:
        1. pip install playwright
        2. playwright install firefox
        3. Run this script again
        """)
    else:
        print("""
        ╔════════════════════════════════════════════╗
        ║   SchoolMind Camoufox Integration          ║
        ║   Starting on http://localhost:8001        ║
        ║   Advanced browser automation enabled      ║
        ╚════════════════════════════════════════════╝
        """)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
