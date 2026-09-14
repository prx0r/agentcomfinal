"""Research backends: web → GitHub → arXiv → docs. Never raises on failure:
backend errors are recorded as evidence (UNKNOWN source), never crash the loop.

Backends take an injectable `fetcher(url) -> (status, body)` so tests run
hermetic; production default is urllib with a timeout. No auth anywhere.
"""
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def urllib_fetcher(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "agentloop/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


class Backend(object):
    name = "base"

    def search(self, query):
        raise NotImplementedError


class SimBackend(Backend):
    """Deterministic fixture backend for tests/demos. Always available."""

    name = "sim"

    def __init__(self, fixtures=None):
        self.fixtures = fixtures or {}

    def search(self, query):
        q = query.lower()
        for key, hits in self.fixtures.items():
            if key.lower() in q:
                return list(hits)
        return [{"source": "sim", "url": "sim://general",
                 "summary": "baseline approach: decompose claim into leaves "
                            "and prove each with existing primitives"}]


class GitHubBackend(Backend):
    name = "github"

    def __init__(self, fetcher=None, per_page=3):
        self.fetcher = fetcher or urllib_fetcher
        self.per_page = per_page

    def search(self, query):
        url = ("https://api.github.com/search/repositories?q="
               + urllib.parse.quote(query) + "&per_page=%d" % self.per_page)
        status, body = self.fetcher(url)
        if status != 200:
            raise ValueError("github-status:%s" % status)
        out = []
        for item in json.loads(body).get("items", [])[:self.per_page]:
            out.append({"source": "github", "url": item.get("html_url", ""),
                        "summary": "%s — %s" % (item.get("full_name", "?"),
                                                (item.get("description") or "")[:160])})
        return out


class ArxivBackend(Backend):
    name = "arxiv"

    def __init__(self, fetcher=None, max_results=3):
        self.fetcher = fetcher or urllib_fetcher
        self.max_results = max_results

    def search(self, query):
        url = ("https://export.arxiv.org/api/query?search_query=all:"
               + urllib.parse.quote(query) + "&max_results=%d&sortBy=relevance"
               % self.max_results)
        status, body = self.fetcher(url)
        if status != 200:
            raise ValueError("arxiv-status:%s" % status)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        out = []
        for entry in ET.fromstring(body).findall("a:entry", ns)[:self.max_results]:
            title = (entry.findtext("a:title", default="", namespaces=ns) or "")
            link = (entry.findtext("a:id", default="", namespaces=ns) or "")
            out.append({"source": "arxiv", "url": link.strip(),
                        "summary": " ".join(title.split())[:200]})
        return out


def multi_search(query, backends):
    """Query backends in order. Returns (hits, errors); never raises."""
    hits, errors = [], []
    for b in backends:
        try:
            for h in b.search(query) or []:
                h = dict(h)
                h["backend"] = b.name
                hits.append(h)
        except Exception as exc:  # noqa: BLE001 - errors are evidence
            errors.append({"backend": b.name, "error": str(exc)[:200]})
    return hits, errors
