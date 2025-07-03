from rest_framework import serializers
from .models import File

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']

    def validate_file(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in ['pptx', 'docx', 'xlsx']:
            raise serializers.ValidationError("Only .pptx, .docx, and .xlsx files are allowed.")
        return value
