#!/usr/bin/env python3
"""
Cursor Agents 页面自动填写脚本
自动填写表单信息，包括姓名、邮箱、公司等字段
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

class CursorAgentsAutoFiller:
    def __init__(self):
        """初始化自动化填写器"""
        self.driver = None
        self.wait = None
        load_dotenv()  # 加载环境变量
        
    def setup_driver(self):
        """设置Chrome浏览器驱动"""
        chrome_options = Options()
        # 可选：无头模式（不显示浏览器窗口）
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 自动下载并设置ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 设置等待时间
        self.wait = WebDriverWait(self.driver, 10)
        
        # 隐藏自动化特征
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def navigate_to_page(self):
        """导航到Cursor Agents页面"""
        url = "https://cursor.com/cn/agents"
        print(f"正在导航到: {url}")
        self.driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
    def wait_for_page_load(self):
        """等待页面完全加载"""
        try:
            # 等待页面标题或主要元素出现
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("页面加载完成")
        except Exception as e:
            print(f"页面加载超时: {e}")
            
    def find_form_elements(self):
        """查找表单元素"""
        form_elements = {}
        
        # 常见的表单字段选择器
        selectors = {
            'name': ['input[name*="name" i]', 'input[placeholder*="姓名" i]', 'input[placeholder*="name" i]'],
            'email': ['input[type="email"]', 'input[name*="email" i]', 'input[placeholder*="邮箱" i]'],
            'company': ['input[name*="company" i]', 'input[name*="organization" i]', 'input[placeholder*="公司" i]'],
            'phone': ['input[type="tel"]', 'input[name*="phone" i]', 'input[placeholder*="电话" i]'],
            'message': ['textarea', 'input[name*="message" i]', 'input[placeholder*="消息" i]']
        }
        
        for field, selector_list in selectors.items():
            for selector in selector_list:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        form_elements[field] = element
                        print(f"找到 {field} 字段: {selector}")
                        break
                except:
                    continue
                    
        return form_elements
        
    def fill_form(self, form_elements):
        """填写表单"""
        # 从环境变量或默认值获取填写信息
        form_data = {
            'name': os.getenv('CURSOR_NAME', '张三'),
            'email': os.getenv('CURSOR_EMAIL', 'test@example.com'),
            'company': os.getenv('CURSOR_COMPANY', '测试公司'),
            'phone': os.getenv('CURSOR_PHONE', '13800138000'),
            'message': os.getenv('CURSOR_MESSAGE', '我想了解更多关于Cursor Agents的信息')
        }
        
        print("开始填写表单...")
        
        for field, element in form_elements.items():
            if field in form_data:
                try:
                    # 清空字段
                    element.clear()
                    time.sleep(0.5)
                    
                    # 填写信息
                    element.send_keys(form_data[field])
                    print(f"已填写 {field}: {form_data[field]}")
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"填写 {field} 时出错: {e}")
                    
    def submit_form(self):
        """提交表单"""
        try:
            # 查找提交按钮
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("提交")',
                'button:contains("Submit")',
                'button:contains("发送")'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    if 'contains' in selector:
                        # 对于包含文本的按钮，使用XPath
                        text = selector.split('"')[1]
                        submit_button = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if submit_button and submit_button.is_displayed():
                        break
                except:
                    continue
                    
            if submit_button:
                print("找到提交按钮，准备提交...")
                submit_button.click()
                print("表单已提交")
                time.sleep(3)  # 等待提交响应
            else:
                print("未找到提交按钮")
                
        except Exception as e:
            print(f"提交表单时出错: {e}")
            
    def take_screenshot(self, filename="cursor_agents_filled.png"):
        """截图保存"""
        try:
            self.driver.save_screenshot(filename)
            print(f"截图已保存: {filename}")
        except Exception as e:
            print(f"截图失败: {e}")
            
    def run(self):
        """运行自动化流程"""
        try:
            print("启动Cursor Agents自动填写脚本...")
            
            # 设置浏览器驱动
            self.setup_driver()
            
            # 导航到页面
            self.navigate_to_page()
            
            # 等待页面加载
            self.wait_for_page_load()
            
            # 查找表单元素
            form_elements = self.find_form_elements()
            
            if not form_elements:
                print("未找到表单元素，请检查页面结构")
                return
                
            # 填写表单
            self.fill_form(form_elements)
            
            # 截图保存
            self.take_screenshot()
            
            # 提交表单
            self.submit_form()
            
            print("自动化流程完成！")
            
        except Exception as e:
            print(f"运行过程中出错: {e}")
            
        finally:
            # 保持浏览器打开一段时间，然后关闭
            if self.driver:
                print("5秒后关闭浏览器...")
                time.sleep(5)
                self.driver.quit()
                
if __name__ == "__main__":
    # 创建并运行自动化器
    auto_filler = CursorAgentsAutoFiller()
    auto_filler.run()