from rest_framework import serializers
from .models import Code

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['code_text', 'language']

