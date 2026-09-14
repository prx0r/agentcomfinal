"""Append-only jsonl store with hash chain. Evil edits fail loudly."""
import json
import os

from .canonical import canonical, sha12

GENESIS = "GENESIS"


class Store:
    def __init__(self, path):
        self.path = path

    def _lines(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as fh:
            return [ln for ln in fh.read().splitlines() if ln.strip()]

    def append(self, receipt):
        lines = self._lines()
        if lines:
            prev = sha12(canonical(json.loads(lines[-1])))
        else:
            prev = GENESIS
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(canonical({"prev": prev, "receipt": receipt}).decode()
                     + "\n")
        return prev

    def verify_chain(self):
        lines = self._lines()
        prev = GENESIS
        for ln in lines:
            try:
                rec = json.loads(ln)
            except ValueError:
                return False
            if rec.get("prev") != prev:
                return False
            prev = sha12(canonical(rec))
        return True
