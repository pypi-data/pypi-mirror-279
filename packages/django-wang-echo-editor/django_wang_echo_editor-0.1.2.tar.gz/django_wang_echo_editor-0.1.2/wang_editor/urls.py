from django.urls import path

from wang_editor import views

urlpatterns = [
    path('upload/image/', views.upload_image, name='wang_editor_upload_image'),
    path('upload/video/', views.upload_video, name='wang_editor_upload_video'),
]
