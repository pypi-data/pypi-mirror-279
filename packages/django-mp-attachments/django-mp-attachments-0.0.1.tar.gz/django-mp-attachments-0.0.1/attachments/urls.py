
from django.urls import path

from attachments import views


app_name = 'attachments'


urlpatterns = [

    path('upload/', views.upload_image, name='upload'),

]
