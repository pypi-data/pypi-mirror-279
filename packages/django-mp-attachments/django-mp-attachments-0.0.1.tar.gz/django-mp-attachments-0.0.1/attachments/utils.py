import json

from django.conf import settings
from sorl.thumbnail import get_thumbnail


class Image(dict):
    def __init__(self, item):

        try:
            preview_url = get_thumbnail(item["file"], "100x100").url
        except Exception:
            preview_url = None

        super().__init__({
            **item,
            "url": settings.MEDIA_URL + item["file"],
            "preview_url": preview_url,
        })

    def __hash__(self):
        return hash(self["uuid"])


class ImageListObject:
    def __init__(self, items):
        self.items = [Image(item) for item in items]

    def __repr__(self):
        return json.dumps(self.items)

    def __iter__(self):
        return iter(self.sorted_items)

    def __len__(self):
        return len(self.items)

    @property
    def sorted_items(self):
        return list(sorted(self.items, key=lambda x: x.get("order", 0)))

    @property
    def logo(self):
        items = self.sorted_items
        if items:
            return items[0]["file"]
        return None
