import hashlib

class ContextCache:
    def __init__(self):
        self._content: dict[str, str] = {}
        self._hashes: dict[str, str] = {}

    def hash_of(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def get(self, file_path: str) -> str | None:
        return self._content.get(file_path)

    def has_changed(self, file_path: str, content: str) -> bool:
        return self._hashes.get(file_path) != self.hash_of(content)

    def put(self, file_path: str, content: str) -> str:
        h = self.hash_of(content)
        self._content[file_path] = content
        self._hashes[file_path] = h
        return h
