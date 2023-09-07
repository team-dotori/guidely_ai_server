from django.shortcuts import render
from .forms import ImageForm  
from .models import Image
import os
from django.http import JsonResponse

def upload_image(request):
    lines=[]
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            """ 점자 이미지 파일 저장  """
            
            image = form.cleaned_data['image']
            Image.objects.create(image=image)

            """ 점자 이미지 -> 점자 Text """
            os.environ['image'] = str(image)
            os.system("python run_local.py $image")

            """ 필요없는 파일 삭제 & .brl 파일 -> .txt 파일 """            
            image_name = str(image).split(".")[0] #이미지 이름 가져오기 
            os.remove(f'{image_name}.marked.txt')
            os.remove(f'{image_name}.marked.jpg')
            os.remove(f'{image}') 
            os.rename(f'{image_name}.marked.brl',"input.txt")
            
            """ liblouis 컨테이너 실행 Dockerfile"""
            os.system("docker build -t liblouis-image .")
            os.system("docker run -it --name ai liblouis-image")
            
            """ 한글 변환 결과.txt 파일 컨테이너 -> 호스트 """
            os.system("docker cp ai:/home/result.txt result.txt")

            """ 도커 컨테이너 종료 """
            os.system("docker stop ai")
            os.system("docker rm ai")

            """ 결과 파일 정제 """
            file =open("result.txt",'r',encoding ="UTF-8")
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            file.close()

            os.remove("input.txt")
            os.remove("result.txt")

            return JsonResponse({'result':lines}, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})
