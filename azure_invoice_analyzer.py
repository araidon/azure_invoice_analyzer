import pandas as pd
import datetime
import re
import csv
import sys


def read_csv_file(csv_file):
    """
    CSVファイルを読み込んでDataFrameを返す関数
    """
    print(f"・ファイル読み込み開始: {datetime.datetime.now()}")
    df = pd.read_csv(csv_file, encoding="cp932", engine="pyarrow")
    print(f"・ファイル読み込み終了: {datetime.datetime.now()}")
    return df


def process_invoice(df):
    """
    請求書のデータを処理して製品ごとの数量と金額を計算する関数
    """
    product_dict = {}  # 製品・数量・コスト合計用の辞書
    product_dict2 = {}  # サービス簡略化バージョン

    for product, quantity, cost in zip(df["製品 (Product)"], df["数量 (Quantity)"], df["コスト (Cost)"]):
        # 製品名から不要な文字列を削除
        product = re.sub(" - JA ..st", "", product)

        # 製品ごとの数量とコストを計算
        product_dict.setdefault(product, {"数量": 0.0, "コスト": 0.0})
        product_dict[product]["数量"] += quantity
        product_dict[product]["コスト"] += cost

        # 製品名から不要な文字列を削除（サービス簡略化バージョン用）
        product = re.sub(" -.*$", "", product)
        product_dict2[product] = product_dict2.get(product, 0) + cost

    return product_dict, product_dict2


def write_csv(filename, headerstr, data_dict):
    """
    辞書のデータをCSVファイルに書き込む関数
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{headerstr}\n")
        for key, value in data_dict.items():
            if int(value) == 0:
                continue  # 0円はskip
            f.write(f"{key},{int(value)}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("引数が不足しています。Azureの請求書ファイル(csv)のパスを指定してください。")
        sys.exit()

    csv_file = sys.argv[1]  # コマンドライン引数からAzureの請求書ファイル(csv)のパスを取得

    df = read_csv_file(csv_file)
    product_dict, product_dict2 = process_invoice(df)

    print(f"product種類: {len(product_dict)}")
    total_cost = sum(value["コスト"] for value in product_dict.values())
    print(f"金額合計: {total_cost}")

    write_csv("dict2.csv", "製品,金額", product_dict2)
