from django.shortcuts import render
import os
import simplejson
import uuid
import zipfile
from playityourself_web import settings
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def uploadify_script(request):
    ret = "0"
    file = request.FILES.get("Filedata", None)
    if file:
        result, new_name = profile_upload(file)
        if result:
            ret = "1"
        else:
            ret = "2"
        json = {'ret': ret, 'save_name': new_name}
    else:
        json = {'ret': ret, 'save_name': 'null'}
    return HttpResponse(simplejson.dumps(json, ensure_ascii=False))

@csrf_exempt
def profile_upload(file):
    if file:
        path = os.path.join(os.getcwd(), 'index/static/upload')
        file_name = str(uuid.uuid1()) + '-' + file.name
        path_file = os.path.join(path, file_name)
        fp = open(path_file, 'wb')
        for content in file.chunks():
            fp.write(content)
        fp.close( )
        os.system('sheet.exe '+ path + '/' + file_name +  ' ' + path + '/' + file.name)#调用sheet.exe
        fzip = zipfile.ZipFile(path + '/' + file.name + '.zip', 'w', zipfile.ZIP_DEFLATED)
        curNum = 1;
        curFile = path + '/' + file.name + '_' + str(curNum) +'.png'
        while(os.path.exists(curFile)):
            fzip.write(curFile)
            curNum = curNum + 1;
            curFile = path + '/' + file.name + '_' + str(curNum) +'.png'
        fzip.close()
        return (True, file_name)
    return (False, 'Error_File_Name')

@csrf_exempt
def profile_delete(request):
    del_file = request.POST.get("delete_file", '')
    if del_file:
        path_file = os.path.join(settings.MEDIA_ROOT, 'upload', del_file)
        os.remove(path_file)
        #wav  #png

@csrf_exempt
def download(request,file):
    path = os.path.join(os.getcwd(), 'index/static/upload')
    file_name = path + '/' + file
    def read_file(file_name,buf_size = 25536):
        f = open(file_name,'rb')
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    response = HttpResponse(read_file(file_name))
    return response
