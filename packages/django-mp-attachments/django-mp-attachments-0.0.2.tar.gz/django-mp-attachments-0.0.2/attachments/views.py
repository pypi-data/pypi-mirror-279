import uuid
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import urlretrieve

from django.core.files import File
from django.core.files.storage import default_storage
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from attachments.utils import PreviewImageAttachment
from attachments.forms import UploadImageForm


@csrf_exempt
@require_POST
@staff_member_required
def upload_image(request, upload_to):

    form = UploadImageForm(data=request.POST, files=request.FILES)

    if form.is_valid():

        data = form.cleaned_data

        if data.get('url'):
            try:
                result = urlretrieve(data['url'])
                file = File(open(result[0], 'rb'))
            except HTTPError as e:
                error = _('Can not upload {}: {}').format(data['url'], str(e))
                return HttpResponseBadRequest(error)

        elif data.get('file'):
            file = data['file']

        else:
            return HttpResponseBadRequest('No data')

        file_uuid = str(uuid.uuid4())
        ext = file.name.split('.')[-1]
        file_name = f'{upload_to}/{file_uuid}.{ext}'
        default_storage.save(file_name, file)

        return JsonResponse(
            PreviewImageAttachment({
                'uuid': file_uuid,
                'file': file_name,
                'created': datetime.now().isoformat(),
            })
        )

    return HttpResponseBadRequest('Data not valid')
