from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

# class NewVisitorTest(unittest.TestCase):
class NewVisitorTest(LiveServerTestCase):

    def setUp(self):  #打开浏览器，在测试之前运行
        self.browser = webdriver.Chrome()
    def tearDown(self) -> None:  #关闭浏览器，在测试之后运行
        self.browser.quit()
    def wait_for_row_in_list_table(self,row_text):
        # 等待的最长时间
        MAX_WAIT = 10
        start_time = time.time()
        #一直循环，知道遇到两个出口中的一个为止
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
                return #如果上面的通过了，就return
            except (AssertionError,WebDriverException) as e:
                #一旦捕获异常：WebDriverException：页面未加载或者selenium在页面上未找到表格元素时抛出
                #AssertionError：没有我们找的行
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    #赋值方法，不以test开头不会被测试
    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #这个网站有一个在线待办事项应用，去瞧瞧
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        #发现网页的标题和头部都包含"To-Do"这个词
        self.assertIn('To-Do',self.browser.title)
        #Selenium提供查找网页内容的方法find_elements_by_tag_name
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        #她在一个文本框中输入了"Buy peacock feathers"
        # Selenium中输入内容的方法：send_keys
        inputbox.send_keys("Buy peacock feathers")
        #Keys的作用是发送回车键等特殊的案件
        #按下回车键后，页面更新了，待办事项中表格显示了"1：Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)#按下回车键之后页面会刷新，time.slepp的作用是等待页面加载完毕
        self.check_for_row_in_list_table('1:Buy peacock feathers')

        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(any(row.text == '1:Buy peacock feathers' for row in rows),
        #                 f"New to-do item did not appear in table. Contents were:\n {table.text}")
        #self.assertIn('1:Buy peacock feathers',[row.text for row in rows])
        # 页面中又显示了一个文本框，可以输入其他的待办事项
        #她输入了"Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        # self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)#页面更新，清单中有两个待办事项了
        self.check_for_row_in_list_table('1:Buy peacock feathers')
        self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')

        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn('1:Buy peacock feathers', [row.text for row in rows])
        #self.assertIn('2:Use peacock feathers to make a fly', [row.text for row in rows])

        #想看到网站记住自己的清单并别生成唯一的url
        #用户不能相互查看各自的清单，每个用户都有自己的Url，能访问自己的清单
        # self.fail('Finish the test!') #提醒测试结束了

    # def test_can_start_a_list_for_one_user(self):
    #     self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')
    #     self.wait_for_row_in_list_table('1:Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #新建一个待办事项
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1:Buy peacock feathers')
        #清单有唯一的url
        edith_list_url = self.browser.current_url
        #检车字符串是否匹配正则表达式
        self.assertRegex(edith_list_url,'/lists/.+')

        self.browser.quit()
        #新用户弗朗西斯访问了网站
        #使用一个新的浏览器会话
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        #页面中看不到edith的清单
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly',page_text)
        #弗朗西斯输入一个新的待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
        #弗朗西斯获得了他唯一的url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)
        #弗朗西斯这个页面也没有edith的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

# if __name__ == '__main__': #检查自己是都在命令行中运行，而不是在其他脚本中导入
#     unittest.main()
