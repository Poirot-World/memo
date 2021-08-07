from selenium import webdriver
import unittest
class NewVisitorTest(unittest.TestCase):
    def setUp(self):  #打开浏览器，在测试之前运行
        self.browser = webdriver.Chrome()
    def tearDown(self) -> None:  #关闭浏览器，在测试之后运行
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do',self.browser.title)
        self.fail('Finish the test!') #提醒测试结束了

if __name__ == '__main__': #检查自己是都在命令行中运行，而不是在其他脚本中导入
    unittest.main()
