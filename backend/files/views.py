from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializers import FileUploadSerializer
from .utils import encrypt_id, decrypt_id

# Upload File (OPS only)
# class FileUploadView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if request.user.user_type != 'OPS':
#             return Response({"error": "Only OPS users can upload files."}, status=403)

#         serializer = FileUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(uploaded_by=request.user)
#             return Response({"message": "File uploaded successfully."}, status=201)
#         return Response(serializer.errors, status=400)


from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import File

import os
import re
import requests
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import File

class FileUploadView(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if request.user.user_type != 'OPS':
            return Response({"error": "Only Ops users can upload files."}, status=403)

        file_url = request.data.get("file_url")

        if not file_url:
            return Response({"error": "file_url is required."}, status=400)

        allowed_extensions = ['.pptx', '.docx', '.xlsx']

        try:
            # ✅ Handle Google Docs/Sheets/Slides
            if "docs.google.com" in file_url:
                match = re.search(r"/d/([a-zA-Z0-9_-]+)", file_url)
                if not match:
                    return Response({"error": "Invalid Google Docs URL format."}, status=400)
                file_id = match.group(1)

                if "document" in file_url:
                    file_url = f"https://docs.google.com/document/d/{file_id}/export?format=docx"
                    filename = f"{file_id}.docx"
                elif "spreadsheets" in file_url:
                    file_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
                    filename = f"{file_id}.xlsx"
                elif "presentation" in file_url:
                    file_url = f"https://docs.google.com/presentation/d/{file_id}/export?format=pptx"
                    filename = f"{file_id}.pptx"
                else:
                    return Response({"error": "Unsupported Google Docs file type."}, status=400)

            elif "drive.google.com" in file_url:
                match = re.search(r"/d/([a-zA-Z0-9_-]+)", file_url)
                if match:
                    file_id = match.group(1)
                    file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    filename = f"{file_id}"
                else:
                    return Response({"error": "Invalid Google Drive URL format."}, status=400)

            else:
                # fallback for direct links
                filename = os.path.basename(file_url.split("?")[0])

            # ✅ Validate file extension
            if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
                return Response({"error": "Invalid file type. Only .pptx, .docx, .xlsx allowed."}, status=400)

            # ✅ Download the file
            response = requests.get(file_url)
            response.raise_for_status()

            # ✅ Save to DB
            content_file = ContentFile(response.content, name=filename)
            File.objects.create(uploaded_by=user, file=content_file)

            return Response({"message": "File fetched and uploaded successfully."}, status=201)

        except requests.RequestException:
            return Response({"error": "Failed to fetch file from the provided URL."}, status=400)

# Generate Secure Link (CLIENT only)
class GenerateDownloadLink(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        if request.user.user_type != 'CLIENT':
            return Response({"error": "Only CLIENT users can generate download links."}, status=403)

        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({"error": "File not found."}, status=404)

        encrypted_id = encrypt_id(file.id)
        download_link = request.build_absolute_uri(f"/api/download-file/{encrypted_id}/")

        return Response({
            "download-link": download_link,
            "message": "success"
        })

# Actual File Download API (CLIENT only)
from django.http import FileResponse
import os

class DownloadFile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, encrypted_id):
        if request.user.user_type != 'CLIENT':
            return Response({"error": "Access denied."}, status=403)
        
        try:
            file_id = decrypt_id(encrypted_id)
            file = File.objects.get(id=file_id)
        except Exception:
            return Response({"error": "Invalid or expired link."}, status=400)

        file_path = file.file.path
        if not os.path.exists(file_path):
            return Response({"error": "File not found."}, status=404)

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

# List All Files (CLIENT only)
class ListFiles(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'CLIENT':
            return Response({"error": "Only CLIENT users can list files."}, status=403)
        
        files = File.objects.all().order_by('-uploaded_at')
        serializer = FileUploadSerializer(files, many=True)
        return Response(serializer.data)
from django.shortcuts import render

# Create your views here.
