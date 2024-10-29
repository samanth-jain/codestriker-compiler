from django.urls import path
from . import views
urlpatterns = [
    path('code-compiler/', views.codeapipost, name='code_compiler'),
    # path('submit-code/', views.code_editor, name='submit_code'),  # Using the same view for simplicity
]