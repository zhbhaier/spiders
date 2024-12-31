import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    driver.maximize_window()
    return driver

def search_keyword(driver, keyword):
    driver.get('https://www.taobao.com')
    wait = WebDriverWait(driver, 10)
    key = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    key.send_keys(keyword)
    submit.click()
    time.sleep(20)

def scroll_and_load(driver):
    for _ in range(20):  # 假设滚动5次
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 等待加载

def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('div', class_='doubleCard--gO3Bz6bu')
    data_list = []

    for index, item in enumerate(items, start=1):
        title = item.find('div', class_='title--qJ7Xg_90').get_text(strip=True) if item.find('div', class_='title--qJ7Xg_90') else ''
        price = item.find('span', class_='priceInt--yqqZMJ5a').get_text(strip=True) if item.find('span', class_='priceInt--yqqZMJ5a') else ''
        deal = item.find('span', class_='realSales--XZJiepmt').get_text(strip=True) if item.find('span', class_='realSales--XZJiepmt') else ''
        location = item.find('div', class_='procity--wlcT2xH9').get_text(strip=True) if item.find('div', class_='procity--wlcT2xH9') else ''
        shop = item.find('span', class_='shopNameText--DmtlsDKm').get_text(strip=True) if item.find('span', class_='shopNameText--DmtlsDKm') else ''
        url = item.find('a', href=True)['href'] if item.find('a', href=True) else ''
        shop_url = item.find('a', class_='shopName--hdF527QA')['href'] if item.find('a', class_='shopName--hdF527QA') else ''
        
        img_tag = item.find('img', class_='iconPic--pZyhTNNV')
        img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''

        data = {
            "Page": 1,  # 假设为第一页
            "Num": index,
            "title": title,
            "price": price,
            "deal": deal,
            "location": location,
            "shop": shop,
            "sPostFre": "包邮",  # 假设为包邮
            "url": url,
            "shop_url": shop_url,
            "img_url": img_url
        }

        data_list.append(data)
    
    return data_list

def save_to_excel(data_list):
    df = pd.DataFrame(data_list)
    df.to_excel('products.xlsx', index=False)
    print("数据已保存到 products.xlsx")

def main():
    keyword = input("请输入搜索商品名称: ")
    driver = setup_driver()
    search_keyword(driver, keyword)
    scroll_and_load(driver)
    data_list = extract_data(driver)
    save_to_excel(data_list)
    driver.quit()

if __name__ == '__main__':
    main()


