"""
Selenium-based web parser for JavaScript-heavy websites.
This is an optional parser that requires selenium to be installed.
"""

from __future__ import annotations
from typing import Iterable, Set, List, Deque, Optional, Dict, Any
from collections import deque
from urllib.parse import urljoin, urlparse
import time
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class SeleniumWebParser(ParserProtocol):
    name = "selenium_web"
    content_types: Iterable[str] = ("text/html",)
    extensions: Iterable[str] = ()

    def can_parse(self, meta: Metadata) -> bool:
        # Only handle URLs (http/https) here
        src = meta.source or ""
        return src.startswith("http://") or src.startswith("https://")

    def parse(self, target, meta: Metadata, recursive: bool = False, max_links: int = 50, max_depth: int = 1, same_origin: bool = True, delay: float = 1.0, headless: bool = True, **kwargs) -> UnifiedDocument:
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.common.exceptions import TimeoutException, WebDriverException
            from bs4 import BeautifulSoup
        except ImportError:
            # Fallback to regular web parser if selenium is not available
            from .web import WebParser
            web_parser = WebParser()
            return web_parser.parse(target, meta, recursive, max_links, max_depth, same_origin, delay, **kwargs)

        start_url = str(target)
        doc = UnifiedDocument(meta=meta, sections=[])
        seen: Set[tuple[str, int]] = set()
        q: Deque[tuple[str, int]] = deque([(start_url, 0)])
        parsed_start = urlparse(start_url)
        origin = f"{parsed_start.scheme}://{parsed_start.netloc}"

        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        count = 0
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)
            
            while q and (not recursive or count == 0 or (recursive and count < max_links)):
                url, depth = q.popleft()
                if (url, depth) in seen:
                    continue
                seen.add((url, depth))
                
                try:
                    # Navigate to the page
                    driver.get(url)
                    
                    # Wait for page to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # Additional wait for dynamic content
                    time.sleep(2)
                    
                    # Get page source after JavaScript execution
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "lxml")
                    
                    # Extract page information
                    page_info = self._extract_page_info(soup, url)
                    
                    if page_info["title"] and not doc.meta.title:
                        doc.meta.title = page_info["title"]
                    
                    # Create section for this page
                    if page_info["content"]:
                        section = Section(
                            heading=page_info["title"] or f"Page {count + 1}",
                            chunks=[Chunk(text=page_info["content"], order=count, meta={"url": url, "depth": depth})],
                            meta={"url": url, "depth": depth, "word_count": len(page_info["content"].split())}
                        )
                        doc.sections.append(section)
                    
                    # Extract links for recursive crawling
                    if recursive and depth < max_depth:
                        links = self._extract_links(soup, url, parsed_start, same_origin)
                        for link in links:
                            if (link, depth + 1) not in seen:
                                q.append((link, depth + 1))
                    
                    count += 1
                    
                    if delay:
                        time.sleep(delay)
                        
                except TimeoutException:
                    error_section = Section(
                        heading=f"Timeout loading {url}",
                        chunks=[Chunk(text=f"Page load timeout after 30 seconds", order=count, meta={"error": True, "url": url})],
                        meta={"error": True, "url": url}
                    )
                    doc.sections.append(error_section)
                    count += 1
                    continue
                    
                except WebDriverException as e:
                    error_section = Section(
                        heading=f"Error loading {url}",
                        chunks=[Chunk(text=f"WebDriver error: {str(e)}", order=count, meta={"error": True, "url": url})],
                        meta={"error": True, "url": url}
                    )
                    doc.sections.append(error_section)
                    count += 1
                    continue
                    
                if count >= max_links:
                    break
                    
        except Exception as e:
            error_section = Section(
                heading="Selenium Web Parser Error",
                chunks=[Chunk(text=f"Failed to initialize Selenium: {str(e)}", order=0, meta={"error": True})],
                meta={"error": True}
            )
            doc.sections.append(error_section)
        finally:
            try:
                driver.quit()
            except:
                pass
                
        doc.meta.extra["pages_parsed"] = count
        depths = [depth for _, depth in seen if depth > 0]
        doc.meta.extra["crawl_stats"] = {
            "total_pages": count,
            "max_depth_reached": max(depths) if depths else 0,
            "unique_domains": len(set(urlparse(url).netloc for url, _ in seen))
        }
        return doc
    
    def _extract_page_info(self, soup, url: str) -> Dict[str, Any]:
        """Extract comprehensive information from a web page."""
        info = {
            "title": None,
            "content": "",
            "meta": {},
            "links": [],
            "images": []
        }
        
        # Extract title
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            info["title"] = title_tag.string.strip()
        
        # Extract meta information
        for meta in soup.find_all("meta"):
            name = meta.get("name") or meta.get("property") or meta.get("http-equiv")
            content = meta.get("content")
            if name and content:
                info["meta"][name] = content
        
        # Extract main content (improved content extraction)
        content_selectors = [
            "main", "article", "[role='main']", ".content", "#content",
            ".main-content", ".post-content", ".entry-content", ".page-content"
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find("body") or soup
        
        # Extract text content with better structure
        content_parts = []
        
        # Extract headings and paragraphs
        for element in main_content.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "li", "blockquote", "span"]):
            text = element.get_text(" ", strip=True)
            if text and len(text) > 10:  # Filter out very short text
                content_parts.append(text)
        
        info["content"] = "\n\n".join(content_parts)
        
        # Extract links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)
            if href and text:
                info["links"].append({"url": href, "text": text})
        
        # Extract images
        for img in soup.find_all("img", src=True):
            src = img["src"]
            alt = img.get("alt", "")
            if src:
                info["images"].append({"src": src, "alt": alt})
        
        return info
    
    def _extract_links(self, soup, current_url: str, parsed_start, same_origin: bool) -> List[str]:
        """Extract and normalize links from the page."""
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(current_url, href)
            parsed_link = urlparse(full_url)

            if same_origin and parsed_link.netloc != parsed_start.netloc:
                continue

            # Basic filtering for common non-content links
            if any(ext in parsed_link.path.lower() for ext in [".pdf", ".zip", ".rar", ".exe", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]):
                continue
            if full_url.startswith("mailto:") or full_url.startswith("tel:"):
                continue

            links.append(full_url)
        return list(set(links))

# Register the parser
register_parser(SeleniumWebParser())
