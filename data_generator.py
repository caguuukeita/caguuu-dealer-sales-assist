# data_generator.py
# ダミーの products.csv を生成します（UTF-8）
# 実行: python data_generator.py

import csv
from pathlib import Path

OUTPUT = Path("products.csv")

def main():
    rows = [
        {
            "category": "ベッド",
            "product_name": "跳ね上げ式収納ベッド",
            "price": 85000,
            "sales_point": "★布団も入る大容量収納！\n★女性でも軽く持ち上がるガス圧式\n★通気性の良い床板で湿気対策",
            "ec_url": "https://caguuu.com/products/bed01",
            "image_url": "https://placehold.jp/200x200.png?text=Bed01",
        },
        {
            "category": "ベッド",
            "product_name": "コンセント付き宮棚ベッド",
            "price": 69000,
            "sales_point": "★スマホ充電OK！宮棚＋コンセント付き\n★圧迫感が少ないシンプルデザイン\n★組立てしやすい設計",
            "ec_url": "https://caguuu.com/products/bed02",
            "image_url": "https://placehold.jp/200x200.png?text=Bed02",
        },
        {
            "category": "ソファ",
            "product_name": "3人掛けレザーソファ",
            "price": 120000,
            "sales_point": "★傷に強い新素材レザー使用\n★ペットがいても安心\n★お手入れはサッと拭くだけ",
            "ec_url": "https://caguuu.com/products/sofa01",
            "image_url": "https://placehold.jp/200x200.png?text=Sofa01",
        },
        {
            "category": "ソファ",
            "product_name": "ゆったりカウチソファ（右カウチ）",
            "price": 158000,
            "sales_point": "★足を伸ばせるカウチでくつろぎ最大\n★座面が広く家族で使いやすい\n★カバーは外してお手入れ可能（※仕様に応じて）",
            "ec_url": "https://caguuu.com/products/sofa02",
            "image_url": "https://placehold.jp/200x200.png?text=Sofa02",
        },
        {
            "category": "テーブル",
            "product_name": "昇降リビングテーブル",
            "price": 49800,
            "sales_point": "★食事もPC作業もこれ1台\n★高さ調整で姿勢がラク\n★収納スペース付きで散らかりにくい",
            "ec_url": "https://caguuu.com/products/table01",
            "image_url": "https://placehold.jp/200x200.png?text=Table01",
        },
        {
            "category": "テーブル",
            "product_name": "丸型ダイニングテーブル（4人用）",
            "price": 78000,
            "sales_point": "★角がなく安心、動線がスムーズ\n★会話がしやすい丸テーブル\n★木目がきれいで部屋が明るく見える",
            "ec_url": "https://caguuu.com/products/table02",
            "image_url": "https://placehold.jp/200x200.png?text=Table02",
        },
    ]

    fieldnames = ["category", "product_name", "price", "sales_point", "ec_url", "image_url"]

    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"✅ Generated: {OUTPUT.resolve()}  (rows={len(rows)})")

if __name__ == "__main__":
    main()