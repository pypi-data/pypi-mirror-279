from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from pathlib import Path
import importlib
import os


def upload_file(file):
    storage_backend_path = settings.WANG_EDITOR_CONFIG.get('storage_backend', None)
    if storage_backend_path:
        module_path, class_name = storage_backend_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        storage_backend = getattr(module, class_name)
        storage_instance = storage_backend()
        link = storage_instance.save(file.name, file)
    else:
        media_url = settings.MEDIA_URL
        media_root = settings.MEDIA_ROOT
        upload = settings.WANG_EDITOR_CONFIG.get('upload', 'upload')
        if not media_url:
            raise Exception('媒体资源URL不存在,请在settings.py中配置MEDIA_URL')
        if not media_root:
            raise Exception('媒体资源存储路径不存在,请在settings.py中配置MEDIA_ROOT')

        if not os.path.exists(media_root):
            os.makedirs(media_root)
        file_path = os.path.join(media_root, upload, file.name)  # 上传的图片的路径,本地存储路径
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        link = Path(media_url, upload, file.name).as_posix()
    return link


# Create your views here.
@csrf_exempt
def upload_image(request):
    try:
        image = request.FILES.get('wangeditor-uploaded-image')
        link = upload_file(image)
        return JsonResponse(
            data={
                'errno': 0,
                'data': {
                    'url': link,
                    'alt': image.name,
                    'href': link
                }
            }
        )
    except Exception as e:
        return JsonResponse(
            data={
                'errno': 1,
                'message': str(e)
            }
        )


@csrf_exempt
def upload_video(request):
    try:
        video = request.FILES.get('wangeditor-uploaded-video')
        link = upload_file(video)
        return JsonResponse(data={
            'errno': 0,
            'data': {
                'url': link,
            }
        })
    except Exception as e:
        return JsonResponse(data={
            'errno': 1,
            'message': str(e)
        })
