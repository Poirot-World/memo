from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Create your tests here.
class HomePageTest(TestCase):
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)


    def test_uses_home_template(self):
        #request = HttpRequest() #创建了一个HttpRequest对象。用户请求网页，django中看到的就是这个对象
        #response = home_page(request)#把这个httprequest对象传给home_page视图，得到响应。
        #用test client代替httpresponse对象，也不再直接调用视图函数，用self,client.get
        response = self.client.get('/')
        html = response.content.decode('utf8')#提取响应的.content，得到的结果是原始字节，即0和1。
        #expected_html = render_to_string('home.html') #用render_to_String手动渲染
        #self.assertEqual(html,expected_html)
        # decode用来把原始字节转换成发给用户的html字符串
        # self.assertTrue(html.startswith('<html>')) #希望响应以<html>标签开头，并在结尾处关闭该标签
        # self.assertIn('<title>To-Do lists</title>', html)#希望响应中有一个<title>标签，内容包含单词To-Do Lists
        # self.assertTrue(html.endswith('</html>'))#希望响应以</html>标签结尾
        self.assertTemplateUsed(response,'home.html') #assertTemplateUsed用于检查响应是哪个模板渲染的

    def test_can_save_a_post_request(self):
        #发送post请求，data指定想发送的表单数据
        response = self.client.post('/',data= {'item_text':'A new list item'})
        #检查post请求渲染得到的html中是否有指定的文本
        self.assertIn('A new list item',response.content.decode())
        self.assertTemplateUsed(response, 'home.html')  # 检查是否依然使用这个模板


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        #	3. 在数据库中创建新纪录：创建一个对象；为一些属性赋值；调用.save()函数
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        #django提供了一个查询数据库的API,即类.objects，.all()是查询方法，返回类似列表的对象，叫QuerySet
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(second_saved_item.text,'Item the second')
