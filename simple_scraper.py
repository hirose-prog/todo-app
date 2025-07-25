import requests
from bs4 import BeautifulSoup
import json
import csv

# アクセスしたいWebサイトのURL
# Amazonの検索結果ページを例とします。ご自身の環境で検索したURLに置き換えてもOKです。
url = "https://www.amazon.co.jp/s?k=python+%E6%9C%AC"

# データを保存するファイル名
SAVE_FILE_JSON = "amazon_products.json"
SAVE_FILE_CSV = "amazon_products.csv"

try:
    # WebサイトにアクセスしてHTMLデータを取得する
    response = requests.get(url)
    # HTTPエラーが発生した場合に例外を発生させる (例: 404 Not Foundなど)
    response.raise_for_status()
    # 文字化け対策 (サイトのエンコーディングを自動判別)
    response.encoding = response.apparent_encoding

    # 取得したHTMLデータをBeautifulSoupで解析する
    soup = BeautifulSoup(response.text, 'html.parser')

    # Webページのタイトルを取得する
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        print(f"Webページのタイトル: {title}")
    else:
        print("タイトルタグが見つかりませんでした。")

    print("\n--- Amazonの商品名とURL ---")

    # 商品のデータを格納するリスト
    all_product_data = []

    # Amazonの商品名を探す
    # <a>タグでclassが"s-underline-text"のものをすべて見つけ出す
    # これが商品タイトルへのリンクになっていることが多いです。
    product_links = soup.find_all('a', class_='s-underline-text')

    if product_links:
        print(f"見つかったリンクの数: {len(product_links)}個")

        for i, product_link in enumerate(product_links):
            # リンクのテキスト（商品名であることが多い）を取得
            product_name = product_link.get_text(strip=True)

            # リンクのURLを取得
            product_url = product_link.get('href')

            # 相対URLの場合（例: /Nintendo-Switch-...）は絶対URLに変換
            # product_urlがNoneでないことを確認してから処理します
            if product_url and product_url.startswith('/'):
                product_url = requests.compat.urljoin(url, product_url)

            # 取得した商品名とURLをターミナルに表示
            print(f"{i+1}. {product_name}")
            print(f"   URL: {product_url}")

            # 取得したデータを辞書としてリストに追加
            # 今回は、商品名とURLが両方とも存在し、URLに"http"が含まれる基本的なフィルターを追加
            if product_name and product_url and "http" in product_url:
                product_item = {
                    "name": product_name,
                    "url": product_url
                }
                all_product_data.append(product_item)

        # --- ここからファイル保存の処理 ---

        # 1. データをJSONファイルに保存する
        with open(SAVE_FILE_JSON, 'w', encoding='utf-8') as f:
            json.dump(all_product_data, f, indent=2, ensure_ascii=False) # indentを2に設定
        print(f"\n取得した商品をJSON形式で '{SAVE_FILE_JSON}' に保存しました。")

        # 2. データをCSVファイルに保存する
        with open(SAVE_FILE_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # CSVのヘッダー（列の名前）を書き込む
            writer.writerow(['Product Name', 'Link'])

            # 各商品のデータをCSVに書き込む
            for item in all_product_data:
                writer.writerow([item['name'], item['url']])
        print(f"取得した商品をCSV形式で '{SAVE_FILE_CSV}' に保存しました。")

    else:
        print("商品情報が見つかりませんでした。")

except requests.exceptions.RequestException as e:
    print(f"Webサイトへのアクセス中にエラーが発生しました: {e}")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")