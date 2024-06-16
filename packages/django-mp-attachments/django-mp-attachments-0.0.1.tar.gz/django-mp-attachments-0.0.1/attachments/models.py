import shutil

from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage
from django.db.models import JSONField

from attachments.forms import ImageListFormField
from attachments.utils import ImageListObject


class ImageListField(ArrayField):
    def __init__(self, verbose_name=None, upload_to=None, **kwargs):
        self.upload_to = upload_to
        super().__init__(
            JSONField(
                blank=True,
                null=True,
                default=dict,
            ),
            verbose_name=verbose_name,
            blank=True,
            null=True,
        )

    def formfield(self, **kwargs):
        return ImageListFormField(label=self.verbose_name, **kwargs)

    def _from_db_value(self, value, expression, connection):
        if value is None:
            return ImageListObject([])
        items = [
            self.base_field.from_db_value(item, expression, connection)
            for item in value
        ]
        return ImageListObject(items)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return value
        return super().get_db_prep_value(value.sorted_items, connection, prepared)

    def save_form_data(self, instance, data):
        old_images = set(instance.images)
        new_images = set(data)

        added_images = new_images - old_images
        for item in added_images:
            old_path = default_storage.path(item["file"])
            ext = old_path.split(".")[-1]
            new_file_name = f"{self.upload_to}/{item['uuid']}.{ext}"
            new_path = default_storage.path(new_file_name)
            shutil.move(old_path, new_path)
            item["file"] = new_file_name

        removed_images = old_images - new_images
        for item in removed_images:
            try:
                default_storage.delete(item["file"])
            except FileNotFoundError:
                pass

        return super().save_form_data(instance, data)
