#!/usr/bin/env python3
"""
高级 Cursor Agents 页面自动填写脚本
支持多种浏览器，更好的错误处理和自定义配置
"""

import time
import os
import json
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cursor_agents_auto.log'),
        logging.StreamHandler()
    ]
)

class AdvancedCursorAgentsAutoFiller:
    def __init__(self, browser_type='chrome', headless=False):
        """
        初始化高级自动化填写器
        
        Args:
            browser_type (str): 浏览器类型 ('chrome', 'firefox', 'edge')
            headless (bool): 是否使用无头模式
        """
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.driver = None
        self.wait = None
        self.logger = logging.getLogger(__name__)
        
        # 加载配置
        self.load_config()
        
    def load_config(self):
        """加载配置文件"""
        load_dotenv()
        
        # 默认配置
        self.config = {
            'url': 'https://cursor.com/cn/agents',
            'wait_timeout': 10,
            'page_load_delay': 3,
            'field_delay': 0.5,
            'submit_delay': 3,
            'close_delay': 5,
            'form_data': {
                'name': os.getenv('CURSOR_NAME', '张三'),
                'email': os.getenv('CURSOR_EMAIL', 'test@example.com'),
                'company': os.getenv('CURSOR_COMPANY', '测试公司'),
                'phone': os.getenv('CURSOR_PHONE', '13800138000'),
                'message': os.getenv('CURSOR_MESSAGE', '我想了解更多关于Cursor Agents的信息')
            }
        }
        
        # 尝试加载配置文件
        config_file = Path('config.json')
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                self.logger.info("已加载配置文件")
            except Exception as e:
                self.logger.warning(f"加载配置文件失败: {e}")
                
    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            if self.browser_type == 'chrome':
                self.driver = self._setup_chrome()
            elif self.browser_type == 'firefox':
                self.driver = self._setup_firefox()
            elif self.browser_type == 'edge':
                self.driver = self._setup_edge()
            else:
                raise ValueError(f"不支持的浏览器类型: {self.browser_type}")
                
            # 设置等待时间
            self.wait = WebDriverWait(self.driver, self.config['wait_timeout'])
            
            # 隐藏自动化特征
            self._hide_automation_features()
            
            self.logger.info(f"成功设置 {self.browser_type} 浏览器驱动")
            
        except Exception as e:
            self.logger.error(f"设置浏览器驱动失败: {e}")
            raise
            
    def _setup_chrome(self):
        """设置Chrome浏览器"""
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
        
    def _setup_firefox(self):
        """设置Firefox浏览器"""
        options = FirefoxOptions()
        if self.headless:
            options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
        
    def _setup_edge(self):
        """设置Edge浏览器"""
        options = EdgeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
        
    def _hide_automation_features(self):
        """隐藏自动化特征"""
        try:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")
        except Exception as e:
            self.logger.warning(f"隐藏自动化特征失败: {e}")
            
    def navigate_to_page(self):
        """导航到目标页面"""
        try:
            self.logger.info(f"正在导航到: {self.config['url']}")
            self.driver.get(self.config['url'])
            time.sleep(self.config['page_load_delay'])
        except Exception as e:
            self.logger.error(f"导航失败: {e}")
            raise
            
    def wait_for_page_load(self):
        """等待页面完全加载"""
        try:
            # 等待页面标题或主要元素出现
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.logger.info("页面加载完成")
        except Exception as e:
            self.logger.warning(f"页面加载超时: {e}")
            
    def find_form_elements(self):
        """查找表单元素"""
        form_elements = {}
        
        # 扩展的表单字段选择器
        selectors = {
            'name': [
                'input[name*="name" i]', 'input[placeholder*="姓名" i]', 'input[placeholder*="name" i]',
                'input[id*="name" i]', 'input[class*="name" i]'
            ],
            'email': [
                'input[type="email"]', 'input[name*="email" i]', 'input[placeholder*="邮箱" i]',
                'input[id*="email" i]', 'input[class*="email" i]'
            ],
            'company': [
                'input[name*="company" i]', 'input[name*="organization" i]', 'input[placeholder*="公司" i]',
                'input[id*="company" i]', 'input[class*="company" i]'
            ],
            'phone': [
                'input[type="tel"]', 'input[name*="phone" i]', 'input[placeholder*="电话" i]',
                'input[id*="phone" i]', 'input[class*="phone" i]'
            ],
            'message': [
                'textarea', 'input[name*="message" i]', 'input[placeholder*="消息" i]',
                'textarea[placeholder*="留言" i]', 'textarea[placeholder*="message" i]'
            ]
        }
        
        for field, selector_list in selectors.items():
            for selector in selector_list:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            form_elements[field] = element
                            self.logger.info(f"找到 {field} 字段: {selector}")
                            break
                    if field in form_elements:
                        break
                except Exception as e:
                    self.logger.debug(f"选择器 {selector} 查找失败: {e}")
                    continue
                    
        return form_elements
        
    def fill_form(self, form_elements):
        """填写表单"""
        self.logger.info("开始填写表单...")
        
        for field, element in form_elements.items():
            if field in self.config['form_data']:
                try:
                    # 滚动到元素位置
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)
                    
                    # 清空字段
                    element.clear()
                    time.sleep(self.config['field_delay'])
                    
                    # 填写信息
                    value = self.config['form_data'][field]
                    element.send_keys(value)
                    self.logger.info(f"已填写 {field}: {value}")
                    time.sleep(self.config['field_delay'])
                    
                except Exception as e:
                    self.logger.error(f"填写 {field} 时出错: {e}")
                    
    def submit_form(self):
        """提交表单"""
        try:
            # 扩展的提交按钮选择器
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button[class*="submit" i]',
                'button[id*="submit" i]',
                'button:contains("提交")',
                'button:contains("Submit")',
                'button:contains("发送")',
                'button:contains("确认")',
                'button:contains("Confirm")'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    if 'contains' in selector:
                        text = selector.split('"')[1]
                        submit_button = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if submit_button and submit_button.is_displayed() and submit_button.is_enabled():
                        break
                except:
                    continue
                    
            if submit_button:
                self.logger.info("找到提交按钮，准备提交...")
                # 滚动到按钮位置
                self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(0.5)
                
                submit_button.click()
                self.logger.info("表单已提交")
                time.sleep(self.config['submit_delay'])
            else:
                self.logger.warning("未找到提交按钮")
                
        except Exception as e:
            self.logger.error(f"提交表单时出错: {e}")
            
    def take_screenshot(self, filename=None):
        """截图保存"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"cursor_agents_{timestamp}.png"
            
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"截图已保存: {filename}")
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            
    def run(self):
        """运行自动化流程"""
        try:
            self.logger.info(f"启动 {self.browser_type} 浏览器自动化脚本...")
            
            # 设置浏览器驱动
            self.setup_driver()
            
            # 导航到页面
            self.navigate_to_page()
            
            # 等待页面加载
            self.wait_for_page_load()
            
            # 查找表单元素
            form_elements = self.find_form_elements()
            
            if not form_elements:
                self.logger.warning("未找到表单元素，请检查页面结构")
                self.take_screenshot("no_form_elements.png")
                return
                
            # 填写表单
            self.fill_form(form_elements)
            
            # 截图保存
            self.take_screenshot()
            
            # 提交表单
            self.submit_form()
            
            self.logger.info("自动化流程完成！")
            
        except Exception as e:
            self.logger.error(f"运行过程中出错: {e}")
            if self.driver:
                self.take_screenshot("error_screenshot.png")
            
        finally:
            # 保持浏览器打开一段时间，然后关闭
            if self.driver:
                self.logger.info(f"{self.config['close_delay']}秒后关闭浏览器...")
                time.sleep(self.config['close_delay'])
                self.driver.quit()
                
def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cursor Agents 页面自动填写脚本')
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'edge'], 
                       default='chrome', help='选择浏览器类型')
    parser.add_argument('--headless', action='store_true', help='使用无头模式')
    parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建并运行自动化器
    auto_filler = AdvancedCursorAgentsAutoFiller(
        browser_type=args.browser,
        headless=args.headless
    )
    
    if args.config:
        auto_filler.config_file = args.config
        
    auto_filler.run()
    
if __name__ == "__main__":
    main()