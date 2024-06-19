# MP-attachments

Django image attachments application.

### Installation

Installation:
* add `django-mp-attachments` to `requirements.txt`
* add `attachments` to `INSTALLED_APPS`
* add `path('attachments/', include('attachments.urls')),` to `urls.py`

### Usage
Model:
```
from attachments.models import ImageListField

class MyModel(models.Model):
    images = ImageListField(_("Images"), upload_to='somefolder')
```
