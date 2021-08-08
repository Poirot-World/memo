from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    #return HttpResponse('<html><title>To-Do lists</title></html>')
    #render函数：django会自动在所有的应用目录中搜索名为templates的文件夹
    #然后根据模板中的内容构建一个HttpResponse对象
    return render(request,'home.html') #第一个参数是请求对象，第二个参数是渲染的模板名
