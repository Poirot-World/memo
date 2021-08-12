from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List

# Create your views here.
def home_page(request):

    #视图函数处理post请求
    #return HttpResponse('<html><title>To-Do lists</title></html>')
    #render函数：django会自动在所有的应用目录中搜索名为templates的文件夹
    #然后根据模板中的内容构建一个HttpResponse对象
    # if request.method == 'POST':
        #return HttpResponse(request.POST['item_text'])
        # new_item_text = request.POST['item_text']
        #Item.objects.create(text = new_item_text)

    # else:
    #     new_item_text = ''
    # 第一个参数是请求对象，第二个参数是渲染的模板名，第三个参数是一个字典，把模板变量的名称映射在值上
    # return render(request,'home.html',{'new_item_text':new_item_text,})
    # return render(request,'home.html',{'new_item_text':request.POST.get('item_text',''),})
#dic.get用法：如果字典里没有指定"item_text"，那么返回''

    # #视图函数处理完post请求会重新定向
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list-in-the-world/')

    return render(request,'home.html')

def view_list(request,list_id):
    list_ = List.objects.get(id = list_id)
    # items = Item.objects.filter(list = list_)
    return render(request, 'list.html',{'list':list_})
    # return render(request, 'list.html',{'items':items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list = list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')