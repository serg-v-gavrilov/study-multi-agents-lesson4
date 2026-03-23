from ddgs import DDGS
import trafilatura
import os
from config import Settings, SEARCH_ENGINE


def write_report(filename: str, content: str) -> str:
    os.makedirs(Settings.output_dir, exist_ok=True)
    path = Settings.output_dir + "/" + filename
    open(file=path, mode='wt', encoding="utf-8").write(content)
    return path


def web_search(query: str) -> list[dict]:
    try:
        text = DDGS().text(query, max_results=Settings.max_search_results, backend=SEARCH_ENGINE)
        if text is None:
            return "web_search error: failed to fetch search result"
        return text[:Settings.max_url_content_length]
    except Exception as e:
        return f"web_search error: {type(e).__name__}: {e}"


def read_url(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            return "read_url error: failed to fetch URL"
        text = trafilatura.extract(downloaded)
        if text is None:
            return "read_url error: failed to extract text from page"
        return text[:Settings.max_url_content_length]
    except Exception as e:
        return f"read_url error: {type(e).__name__}: {e}"


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Performs WEB search for given query string and returns list of results "
                "each contains attributes title (page title), href (URL) and body "
                "(snippet — 1-2 sentences from the page). "
                "On failure or out of results returns text \"web_search error: \" and error description."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query string"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_url",
            "description": (
                "Loads and returns text of WEB page for given URL. "
                "On failure returns text \"read_url error: \" and error description."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL of the web page to fetch"}
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_report",
            "description": (
                "Writes a report with the specified content in markdown format to a file "
                "with the specified name. Returns the full path to the created file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the output file"},
                    "content": {"type": "string", "description": "Markdown content of the report"},
                },
                "required": ["filename", "content"],
            },
        },
    },
]

TOOLS_MAP = {
    "web_search": web_search,
    "read_url": read_url,
    "write_report": write_report,
}
