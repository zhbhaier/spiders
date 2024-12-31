import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 全局变量
keyword = input("请输入搜索商品名称: ")

# 启动ChromeDriver服务
options = webdriver.ChromeOptions()

# 关闭自动测试状态显示 // 会导致浏览器报：请停用开发者模式
options.add_experimental_option("excludeSwitches", ['enable-automation'])

# 把chrome设为selenium驱动的浏览器代理；
driver = webdriver.Chrome(options=options)

# 反爬机制（此方法执行时可以注入一段 javascript 代码，这里 source 的值为改注入脚本）
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                       {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})

driver.get('https://www.taobao.com')

# 窗口最大化
driver.maximize_window()

# wait是Selenium中的一个等待类，用于在特定条件满足之前等待一定的时间(这里是15秒)。
# 如果一直到等待时间都没满足则会捕获TimeoutException异常
wait = WebDriverWait(driver, 10)


# 打开页面后会强制停止10秒，请在此时手动扫码登陆


def main():
    params(keyword)


def params(keywords):
    print(f"正在搜索{keywords}，获取页面内容......")
    key = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    key.send_keys(keywords)
    submit.click()
    time.sleep(20)
    print(driver.page_source)


if __name__ == '__main__':
    main()


