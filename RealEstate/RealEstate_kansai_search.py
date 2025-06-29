from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Driverの設定
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36')
options.add_argument('--incognito')
# options.add_argument('--headless=new')
options.add_argument('--blink-settings=imagesEnabled=false')

# Driver構築
service = Service(executable_path=r'C:\Users\aspec\OneDrive\ドキュメント\デスクトップ\Lesson\tools\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

# URLの取得
driver.get('https://www.kensetsu-databank.co.jp/kansai/kensaku/')
sleep(3)

# 検索期間の選択
select_values = {
    's-todoke-year-from': '2025',
    's-todoke-month-from': '01',
    's-todoke-day-from': '01',
    's-todoke-year-to': '2025',
    's-todoke-month-to': '03',
    's-todoke-day-to': '31',
}
for name, value in select_values.items():
    select_elem = driver.find_element(By.NAME, name)
    Select(select_elem).select_by_value(value)
    sleep(1)

# 建設地の選択
area_to_check = ['s-osaka24', 's-kobe9', 's-kyoto11']
for area in area_to_check:
    checkbox = driver.find_element(By.CSS_SELECTOR, f'input[name="{area}"][value="{area}"]')
    checkbox.click()
    sleep(1)

# 主要用途の選択
checkbox = driver.find_element(By.CSS_SELECTOR, f'input[name="s-purpose[]"][value="共同住宅"]')
checkbox.click()
sleep(1)

# 工事種別の選択
checkbox = driver.find_element(By.CSS_SELECTOR, f'input[name="s-type[]"][value="新築"]')
checkbox.click()
sleep(1)

# 面積の選択
space_to_check = ['1', '2', '3']
for value in space_to_check:
    checkbox = driver.find_element(By.CSS_SELECTOR, f'input[name="s-area[]"][value="{value}"]')
    checkbox.click()
    sleep(1)

# 検索ボタンクリック
driver.find_element(By.CSS_SELECTOR, 'input.btn001').click()
sleep(3)

# 検索結果全ページのHTML取得
page_num = 1
dir_name = os.path.dirname(os.path.abspath(__file__))

while True:
    html = driver.page_source

    # ファイル名をページ番号で作成して保存
    file_path = os.path.join(dir_name, 'html', f'page_{page_num}.html')
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[保存] ページ {page_num} を {file_path} に保存しました。")
    page_num += 1

    # 次へボタンがあるか確認し、あればクリック
    try:
        driver.find_element(By.NAME, 'goNext').click()
        sleep(3)
    except NoSuchElementException:
        print("次のページがありません。終了します。")
        break

driver.quit()






