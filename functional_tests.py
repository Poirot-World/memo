from selenium import webdriver
import unittest
class NewVisitorTest(unittest.TestCase):
    def setUp(self):  #打开浏览器，在测试之前运行
        self.browser = webdriver.Chrome()
    def tearDown(self) -> None:  #关闭浏览器，在测试之后运行
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        #这个网站有一个在线待办事项应用，去瞧瞧
        self.browser.get('http://localhost:8000')
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
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)#按下回车键之后页面会刷新，time.slepp的作用是等待页面加载完毕

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1:Buy peacock features' for row in rows))
        # 页面中又显示了一个文本框，可以输入其他的待办事项
        #她输入了"Use peacock feathers to make a fly"

        self.fail('Finish the test!') #提醒测试结束了

if __name__ == '__main__': #检查自己是都在命令行中运行，而不是在其他脚本中导入
    unittest.main()
