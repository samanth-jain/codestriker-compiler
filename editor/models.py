from django.db import models

# Create your models here.

class Code(models.Model):
    id = models.AutoField(primary_key=True)
    code_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=50)
    
