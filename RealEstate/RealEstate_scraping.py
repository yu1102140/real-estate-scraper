from time import sleep
import os

import requests
from bs4 import BeautifulSoup

import gspread
import pandas as pd

# 出力用データ辞書
sheet_keys = [
    "物件番号", "日付", "件名", "地名地番", "住居表示", "構造", "階数（地上）", "階数（地下）",
    "延床面積", "敷地面積", "建築主", "建築主住所", "設計者", "施工者", "着工", "完成", "備考"
]

# 全件のデータ格納リスト
all_data = []
index = 0

# 上階層フォルダの絶対パスを取得
dir_name = os.path.dirname(os.path.abspath(__file__))
# そのフォルダ内のhtmlフォルダのパスを作る
html_dir = os.path.join(dir_name, 'html')
# 各htmlファイルを解析
for filename in os.listdir(html_dir):
    print('='*60)
    print(f'{filename}の処理')
    file_path = os.path.join(html_dir, filename)

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

   # 一覧テーブル内の各リンクから詳細ページを取得
    for tr in soup.select('table.ichi > tbody > tr')[1:]:
        link = tr.select_one('a').get('href').replace('..', '')
        full_url = 'https://www.kensetsu-databank.co.jp/kansai' + link

        r_page = requests.get(full_url)
        r_page.raise_for_status()
        sleep(3)
        page_soup = BeautifulSoup(r_page.content, 'lxml')

        # すべての<th><td>ペアを辞書に格納
        data = {}
        for tr in page_soup.select('table.san-two tr'):
            th = tr.select_one('th')
            td = tr.select_one('td')
            if th and td:
                label = th.text.strip()
                value = td.text.strip()
                data[label] = value

        print("---- 抽出されたデータ ----")
        for k, v in data.items():
            print(f"{k}: {v}")

        # 必要な項目だけを抽出（存在しない場合は空文字）
        filtered_data = {key: data.get(key, "") for key in sheet_keys}
        all_data.append(filtered_data)

        index += 1
        # 結果表示
        print('='*30, index, '='*30)
        for k, v in filtered_data.items():
            print(f"{k}: {v}")


# データフレーム化、googleスプレッドシートに出力
df = pd.DataFrame(all_data)
gc = gspread.service_account(
    filename=r'RealEstate\test.json'
)
sh = gc.create(
    '不動産データ',
    folder_id='1Xq3G6YSMN7IXc_Je3pKDD1hQmuhPPYuK'
)
ws = sh.get_worksheet(0)
ws.update(
    [df.columns.values.tolist()]
    + df.values.tolist()
)
print("✅ Googleスプレッドシートに出力しました")
