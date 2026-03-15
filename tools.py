from langchain_core.tools import tool
from ddgs import DDGS
import trafilatura
import os
from config import Settings

@tool
def write_report(filename: str, content: str) -> str:
    "Writes a report with given content in markdown format to given relative filename. Returns full path to created file."
    os.makedirs(Settings.output_dir, exist_ok=True)
    path=Settings.output_dir+"/"+filename
    open(path, 'w').write(content)
    return path

@tool
def web_search(query: str) -> list[dict]:
    "Performs WEB search for given query string and returns list of results each contains attributes " \
    "title (page title), href (URL) and body (snippet — 1-2 sentences from the page)."
    return DDGS().text(query, max_results=Settings.max_search_results)

@tool
def read_url(url: str) -> str:
    "Loads and returns text of WEB page for given URL. " \
    "On failure returns text \"read_url error: \" and error description."
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
    