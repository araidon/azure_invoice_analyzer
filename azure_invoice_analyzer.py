import pandas as pd
import datetime
import re
import csv
import sys

csv_file = sys.argv[1]  # コマンドライン引数からAzureの請求書ファイル(csv)のパスを取得

print(f"・ファイル読み込み開始: {datetime.datetime.now()}")
df = pd.read_csv(csv_file, encoding="cp932", engine="pyarrow")
print(f"・ファイル読み込み終了: {datetime.datetime.now()}")

product_dict = {} #product・数量・コスト合計用の辞書
product_dict2 = {} #サービス簡略化バージョン

#print(f"・列ループ開始: {datetime.datetime.now()}")
for product, quantity, cost,  in zip(df["製品 (Product)"],df["数量 (Quantity)"],df["コスト (Cost)"]):
    product = re.sub(" - JA ..st","", product)
    product_dict[product] = product_dict.get(product, {"数量":0.0, "コスト":0.0}) + cost
    product_dict[product]["数量"] += quantity
    product_dict[product]["コスト"] += cost

    product = re.sub(" -.*$","", product)
    product_dict2[product] = product_dict2.get(product, 0) + cost

#print(f"・列ループ終了: {datetime.datetime.now()}")
print(f"product種類: {len(product_dict)}")
#print(f"金額合計: {sum(product_dict[0]['コスト'].values())}")

def write_csv(filename: str, headerstr: str, data_dict):
    f = open(filename, 'w', encoding='utf-8')
    f.writelines(f"{headerstr}\n")
    for key,value in data_dict.items():
        if int(value) == 0: continue #0円はskip
        f.writelines(f"{key},{int(value)}\n")
    f.close()

write_csv("dict1.csv","製品,数量,金額",product_dict)
write_csv("dict2.csv","製品,金額",product_dict2)

