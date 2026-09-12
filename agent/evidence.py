"""Evidence: extractive only. claim + url + verbatim snippet + char_offset + sha256 + action_log_ref."""
import hashlib

def make_claim(claim: str, url: str, html: str, snippet: str, action_log_ref: int = 0) -> dict:
    off = html.find(snippet)
    if off < 0:
        raise ValueError("snippet not found verbatim in html")
    sha = hashlib.sha256(snippet.encode("utf-8")).hexdigest()
    return {"claim": claim, "url": url, "snippet_verbatim": snippet,
            "char_offset": off, "sha256": sha, "action_log_ref": action_log_ref}
