from __future__ import annotations
from typing import Iterable, Set, List, Deque, Optional, Dict, Any
from collections import deque
from urllib.parse import urljoin, urlparse
import time
import requests
from urllib import robotparser
from bs4 import BeautifulSoup
import re
from ..types import UnifiedDocument, Metadata, Section, Chunk
from ..core import register_parser, ParserProtocol

class WebParser(ParserProtocol):
    name = "web"
    content_types: Iterable[str] = ("text/html",)
    extensions: Iterable[str] = ()

    def can_parse(self, meta: Metadata) -> bool:
        # Only handle URLs (http/https) here
        src = meta.source or ""
        return src.startswith("http://") or src.startswith("https://")

    def parse(self, target, meta: Metadata, recursive: bool = False, max_links: int = 50, max_depth: int = 1, same_origin: bool = True, delay: float = 0.0, user_agent: str = "panparsex/0.1 (+https://github.com/dhruvildarji/panparsex)", extract_js: bool = False, **kwargs) -> UnifiedDocument:
        start_url = str(target)
        doc = UnifiedDocument(meta=meta, sections=[])
        seen: Set[tuple[str, int]] = set()
        q: Deque[tuple[str,int]] = deque([(start_url, 0)])
        parsed_start = urlparse(start_url)
        origin = f"{parsed_start.scheme}://{parsed_start.netloc}"
        rp = robotparser.RobotFileParser()
        rp.set_url(urljoin(origin, "/robots.txt"))
        try:
            rp.read()
        except Exception:
            pass

        def allowed(u: str) -> bool:
            try:
                return rp.can_fetch(user_agent, u)
            except Exception:
                return True

        count = 0
        session = requests.Session()
        session.headers.update({
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        })
        
        while q and (not recursive or count == 0 or (recursive and count < max_links)):
            url, depth = q.popleft()
            if (url, depth) in seen: 
                continue
            seen.add((url, depth))
            if not allowed(url): 
                continue
                
            try:
                r = session.get(url, timeout=15, allow_redirects=True)
                ctype = r.headers.get("Content-Type", "")
                if "text/html" not in ctype and depth > 0:
                    continue
                    
                # Handle different encodings
                if r.encoding:
                    r.encoding = r.encoding
                else:
                    r.encoding = 'utf-8'
                    
                soup = BeautifulSoup(r.text, "lxml")
                
                # Extract page information
                page_info = self._extract_page_info(soup, url, r)
                
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
                
                # Extract JavaScript content if requested
                if extract_js and page_info["javascript"]:
                    js_section = Section(
                        heading=f"JavaScript from {url}",
                        chunks=[Chunk(text=page_info["javascript"], order=count, meta={"type": "javascript", "url": url})],
                        meta={"type": "javascript", "url": url}
                    )
                    doc.sections.append(js_section)
                
                count += 1
                
                # Extract links for recursive crawling
                if recursive and depth < max_depth:
                    links = self._extract_links(soup, url, parsed_start, same_origin)
                    for link in links:
                        if link not in seen:
                            q.append((link, depth + 1))
                
                if delay:
                    time.sleep(delay)
                    
            except Exception as e:
                # Log error but continue
                error_section = Section(
                    heading=f"Error loading {url}",
                    chunks=[Chunk(text=f"Failed to load: {str(e)}", order=count, meta={"error": True, "url": url})],
                    meta={"error": True, "url": url}
                )
                doc.sections.append(error_section)
                count += 1
                continue
                
            if count >= max_links:
                break
                
        doc.meta.extra["pages_parsed"] = count
        depths = [depth for _, depth in seen if depth > 0]
        doc.meta.extra["crawl_stats"] = {
            "total_pages": count,
            "max_depth_reached": max(depths) if depths else 0,
            "unique_domains": len(set(urlparse(url).netloc for url, _ in seen))
        }
        return doc
    
    def _extract_page_info(self, soup: BeautifulSoup, url: str, response: requests.Response) -> Dict[str, Any]:
        """Extract comprehensive information from a web page."""
        info = {
            "title": None,
            "content": "",
            "javascript": "",
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
            ".main-content", ".post-content", ".entry-content"
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
        for element in main_content.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "li", "blockquote"]):
            text = element.get_text(" ", strip=True)
            if text and len(text) > 10:  # Filter out very short text
                content_parts.append(text)
        
        info["content"] = "\n\n".join(content_parts)
        
        # Extract JavaScript content
        scripts = soup.find_all("script")
        js_parts = []
        for script in scripts:
            if script.string:
                js_parts.append(script.string.strip())
        info["javascript"] = "\n\n".join(js_parts)
        
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
            info["images"].append({"src": src, "alt": alt})
        
        return info
    
    def _extract_links(self, soup: BeautifulSoup, current_url: str, parsed_start, same_origin: bool) -> List[str]:
        """Extract and filter links for crawling."""
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(current_url, href)
            parsed_url = urlparse(full_url)
            
            # Filter links
            if same_origin and parsed_url.netloc != parsed_start.netloc:
                continue
            
            # Skip non-HTML links
            if parsed_url.path and not parsed_url.path.endswith(('.html', '.htm', '.php', '.asp', '.jsp')):
                if '.' in parsed_url.path.split('/')[-1]:  # Has file extension
                    continue
            
            # Skip common non-content URLs
            skip_patterns = [
                r'\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz)$',
                r'\.(jpg|jpeg|png|gif|svg|ico|css|js)$',
                r'#',  # Skip anchors
                r'mailto:',  # Skip email links
                r'tel:',  # Skip phone links
            ]
            
            skip = False
            for pattern in skip_patterns:
                if re.search(pattern, full_url, re.IGNORECASE):
                    skip = True
                    break
            
            if not skip:
                links.append(full_url)
        
        return links

register_parser(WebParser())
