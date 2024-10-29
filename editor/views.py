from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Code
import docker
import os, time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CodeSerializer

client = docker.from_env()
temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'temp_files'))
os.makedirs(temp_dir, exist_ok=True)
temp_file_path = os.path.join(temp_dir, 'temp_script.py')


@api_view(['POST'])
def codeapipost(request):
    serializer = CodeSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        code = serializer.validated_data['code_text']
        lang = serializer.validated_data['language']
        if lang == 'python':
            if not code:
                return Response({'error': 'No code found'}, status=status.HTTP_400_BAD_REQUEST)
            
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(code)

            # Run the code inside the Docker container
            container = client.containers.run(
                'python-compiler',
                f'python /app/temp_files/temp_script.py',
                detach=True,
                stdout=True,
                stderr=True,
                volumes={temp_dir: {'bind': '/app/temp_files', 'mode': 'rw'}}
            )
            container.wait()
            output = container.logs().decode('utf-8')
        else:
            return Response({'message' : f'{lang} not supported as of now'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'output': output}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def code_editor(request):
#     output = ''
#     if request.method == 'POST':
#         code = request.POST.get('code')
#         if code:
#             # temp_file_path = 'temp_script.py'
#             with open(temp_file_path, 'w') as temp_file:
#                 temp_file.write(code)

#             time.sleep(1)

#             # Run the code inside the Docker container
#             container = client.containers.run(
#                 'python-compiler',
#                 f'python /app/temp_files/temp_script.py',
#                 detach=True,
#                 stdout=True,
#                 stderr=True,
#                 volumes={temp_dir: {'bind': '/app/temp_files', 'mode': 'rw'}}
#             )
#             container.wait()
#             output = container.logs().decode('utf-8')
#             print(output)
            
#         else:
#             return HttpResponse('No code submitted')
#     return render(request, 'editor.html', context={'output': output})