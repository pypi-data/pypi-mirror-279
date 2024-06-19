
from django.conf import settings
from sorl.thumbnail import get_thumbnail


class ImageAttachment(dict):
    def __init__(self, item):

        super().__init__({
            **item,
            "url": settings.MEDIA_URL + item["file"],
        })


class PreviewImageAttachment(ImageAttachment):
    def __init__(self, item):

        try:
            preview_url = get_thumbnail(item["file"], "100x100").url
        except Exception:
            preview_url = None

        super().__init__({
            **item,
            "preview_url": preview_url,
        })


class Attachments(list):
    def __init__(self, items):
        super().__init__([ImageAttachment(item) for item in items])

    @property
    def logo(self):
        if len(self):
            return self[0]["file"]
        return None
