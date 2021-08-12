from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


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



    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)

    # def test_displays_all_list_item(self):
    #     Item.objects.create(text = 'itemey 1')
    #     Item.objects.create(text = 'itemey 2')
    #     response = self.client.get('/')
    #     self.assertIn('itemey 1',response.content.decode())
    #     self.assertIn('itemey 2',response.content.decode())


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        #发送post请求，data指定想发送的表单数据
        self.client.post('/',data= {'item_text':'A new list item'})
        #检查视图是否把新添加的待办事项存入数据库
        # self.assertEqual(Item.objects.count(),1)
        #objects.all()[0]
        new_item = Item.objects.first()
        #检查待办事项的文本是否正确
        # self.assertEqual(new_item.text,'A new list item')
        #检查post请求渲染得到的html中是否有指定的文本
        #self.assertIn('A new list item',response.content.decode())
        #self.assertTemplateUsed(response, 'home.html')  # 检查是否依然使用这个模板


        # self.assertEqual(response.status_code,302)
        # self.assertEqual(response['location'],'/')

    def test_redirects_after_POST(self):
        # 不再拿响应中的content属性值和渲染模板的值比较
        # 现在比较重新定向
        response = self.client.post('/lists/new',data= {'item_text':'A new list item'})
        new_list = List.objects.first()
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/')
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response,f'/lists/{new_list.id}/')


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        #	3. 在数据库中创建新纪录：创建一个对象；为一些属性赋值；调用.save()函数
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        #django提供了一个查询数据库的API,即类.objects，.all()是查询方法，返回类似列表的对象，叫QuerySet
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text,'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text,'Item the second')
        self.assertEqual(second_saved_item.list,list_)




class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response,'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = 'itemey 1', list = correct_list)
        Item.objects.create(text = 'itemey 2',list = correct_list)


        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)


        response = self.client.get(f'/lists/{correct_list.id}/')
        # self.assertContains(response,'itemey 1') #判断响应里面包含这个字符串，assertContains会处理字节，不用额外的decode
        # self.assertContains(response,'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        #response.context表示要传入render函数的上下文
        self.assertEqual(response.context['list'],correct_list)



class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data = {'item_text':'A new item for an existing list'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data = {'item_text':'A new item for an existing list'})

        self.assertRedirects(response,f'/lists/{correct_list.id}/')
