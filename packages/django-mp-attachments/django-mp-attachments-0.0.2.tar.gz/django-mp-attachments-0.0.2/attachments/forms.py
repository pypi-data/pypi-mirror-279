import json
import uuid
from datetime import datetime

from django import forms
from django.core.files.storage import default_storage
from django.urls import reverse_lazy

from attachments.utils import Attachments, PreviewImageAttachment


class ImageListWidget(forms.HiddenInput):

    template_name = "attachments/field.html"

    def format_value(self, value):
        if not value:
            value = []

        if isinstance(value, str):
            value = json.loads(value)

        return json.dumps([PreviewImageAttachment(item) for item in value])

    class Media:
        css = {
            'all': [
                'attachments/file-manager.css',
                'dropzone/dropzone.min.css'
            ]
        }
        js = [
            'dropzone/dropzone.min.js',
            'attachments/file-manager.js',
        ]


class ImageListFormField(forms.CharField):

    def __init__(self, upload_to=None, *args, **kwargs):
        super().__init__(
            widget=ImageListWidget(attrs={
                'upload_url': reverse_lazy('attachments:upload', args=[upload_to]),
            }),
            required=False,
            *args,
            **kwargs
        )

    def clean(self, value):
        if not value:
            return []
        try:
            items = json.loads(value)
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid JSON format")

        return Attachments([self._clean_item(item) for item in items])

    def _clean_item(self, item):

        if not item.get("uuid"):
            raise forms.ValidationError("No UUID in item")

        try:
            uuid.UUID(item["uuid"])
        except ValueError:
            raise forms.ValidationError("Invalid UUID value")

        if not item.get("file"):
            raise forms.ValidationError("No file in item")

        if not default_storage.exists(item["file"]):
            raise forms.ValidationError("File not found: " + item["file"])

        try:
            int(item["order"])
        except ValueError:
            raise forms.ValidationError("Invalid order value")

        if not item.get("created"):
            raise forms.ValidationError("No creation timestamp in item")

        try:
            datetime.fromisoformat(item["created"])
        except ValueError:
            raise forms.ValidationError("Invalid timestamp value")

        return {
            "file": item["file"],
            "order": item["order"],
            "created": item["created"],
            "uuid": item["uuid"],
        }


class UploadImageForm(forms.Form):

    url = forms.URLField(required=False)
    file = forms.ImageField(required=False)
