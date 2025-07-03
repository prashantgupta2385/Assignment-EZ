from django.urls import path
from .views import (
    FileUploadView,
    GenerateDownloadLink,
    DownloadFile,
    ListFiles,
    
)

urlpatterns = [
    # path('upload-file/', FileUploadView.as_view(), name="upload-file"),
    path('file-upload/', FileUploadView.as_view(), name='file-upload'),
    path('generate-link/<int:file_id>/', GenerateDownloadLink.as_view(), name="generate-link"),
    path('download-file/<str:encrypted_id>/', DownloadFile.as_view(), name="download-file"),
    path('list-files/', ListFiles.as_view(), name="list-files"),
]
