
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField

from attachments.forms import ImageListFormField
from attachments.utils import Attachments


class ImageListField(ArrayField):
    def __init__(self, verbose_name=None, upload_to=None, **kwargs):
        self.upload_to = upload_to
        super().__init__(
            JSONField(
                default=dict,
            ),
            verbose_name=verbose_name,
            blank=True,
            default=list,
        )

    def formfield(self, **kwargs):
        return ImageListFormField(
            label=self.verbose_name,
            initial=list(),
            upload_to=self.upload_to,
            **kwargs
        )

    def _from_db_value(self, value, expression, connection):
        if value is None:
            return Attachments([])
        items = [
            self.base_field.from_db_value(item, expression, connection)
            for item in value
        ]
        return Attachments(items)
