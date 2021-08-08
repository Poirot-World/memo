from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest() #创建了一个HttpRequest对象。用户请求网页，django中看到的就是这个对象
        response = home_page(request)#把这个httprequest对象传给home_page视图，得到响应。
        html = response.content.decode('utf8')#提取响应的.content，得到的结果是原始字节，即0和1。
        # decode用来把原始字节转换成发给用户的html字符串
        self.assertTrue(html.startswith('<html>')) #希望响应以<html>标签开头，并在结尾处关闭该标签
        self.assertIn('<title>To-Do lists</title>', html)#希望响应中有一个<title>标签，内容包含单词To-Do Lists
        self.assertTrue(html.endswith('</html>'))#希望响应以</html>标签结尾