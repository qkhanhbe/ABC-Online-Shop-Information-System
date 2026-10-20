"""DAO (data) layer: resolves product and query image files on disk."""
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


class ImageStorage:

    def __init__(self, root=DATA_DIR):
        self.root = root

    def path(self, relative):
        return relative if os.path.isabs(relative) else os.path.join(self.root, relative)

    def exists(self, relative):
        return os.path.isfile(self.path(relative))

    def save_upload(self, filename, content):
        """Store an uploaded query photo (web search by image) and return its path."""
        folder = os.path.join(self.root, "uploads")
        os.makedirs(folder, exist_ok=True)
        safe = "".join(ch for ch in os.path.basename(filename) if ch.isalnum() or ch in "._-")
        path = os.path.join(folder, safe or "upload.png")
        with open(path, "wb") as f:
            f.write(content)
        return path
