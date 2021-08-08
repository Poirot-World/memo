from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    #return HttpResponse('<html><title>To-Do lists</title></html>')
    #render函数：django会自动在所有的应用目录中搜索名为templates的文件夹
    #然后根据模板中的内容构建一个HttpResponse对象
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    # 第一个参数是请求对象，第二个参数是渲染的模板名，第三个参数是一个字典，把模板变量的名称映射在值上
    return render(request,'home.html',{'new_item_text':request.POST.get('item_text','')})
#dic.get用法：如果字典里没有指定"item_text"，那么返回''

