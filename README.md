# CAGUUU 接客サポートアプリ (caguuu_dealer_app)

店舗スタッフが接客中に片手で操作し、商品のセールスポイント（接客トーク）の確認やECサイトへのスムーズな誘導を行うための、Streamlit製Webアプリケーションです。

## プロジェクト概要

このプロジェクトは、家具ブランド「CAGUUU（カグー）」の店舗接客を支援するためのツールです。
タブレットやスマートフォンでの利用を想定し、大きな文字や押しやすいボタンなど、片手操作におけるアクセシビリティに配慮したUIデザインを採用しています。

## フォルダ・ファイル構成

プロジェクトのルートディレクトリには、以下のファイルが含まれています。

- **[app.py](file:///Users/keita.ito/Work-CAGUUU/2_Areas/caguuu_dealer_app/app.py)**  
  Streamlitで構築された接客サポートアプリのメインプログラムです。
- **[data_generator.py](file:///Users/keita.ito/Work-CAGUUU/2_Areas/caguuu_dealer_app/data_generator.py)**  
  アプリで表示するためのデモ用の商品データ（`products.csv`）を生成するスクリプトです。
- **[products.csv](file:///Users/keita.ito/Work-CAGUUU/2_Areas/caguuu_dealer_app/products.csv)**  
  アプリで読み込む商品データファイルです（`data_generator.py` を実行すると自動生成されます）。
- **[requirements.txt](file:///Users/keita.ito/Work-CAGUUU/2_Areas/caguuu_dealer_app/requirements.txt)**  
  アプリの動作に必要なPythonパッケージ（Streamlit、Pandas）を定義したファイルです。

---

## セットアップと起動手順

アプリをローカル環境で起動するには、以下の手順を実行します。

### 1. 依存ライブラリのインストール
ターミナルを開き、必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

### 2. デモデータの生成
アプリで表示する商品データを生成します（すでに `products.csv` が存在する場合はスキップ可能です）。

```bash
python data_generator.py
```

### 3. アプリケーションの起動
Streamlitを起動して、ブラウザでアプリを開きます。

```bash
streamlit run app.py
```
起動後、自動的にブラウザが立ち上がり、アプリの画面が表示されます。

---

## 主な機能と特徴

### アクセシビリティ重視の画面設計
フォントサイズを20px以上、ボタンの高さを50px以上に設定し、片手での誤タップを防ぐためのカスタムCSS（[app.py:L14-79](file:///Users/keita.ito/Work-CAGUUU/2_Areas/caguuu_dealer_app/app.py#L14-L79)）が組み込まれています。

### 直感的なカテゴリ・検索機能
「ベッド」「ソファ」などのカテゴリをワンタップで切り替えられるほか、商品名の一部を入力して即座に絞り込みが可能です。

### 接客用トークの表示
各商品の詳細を開くと、店舗スタッフがお客様へ伝えるべき「セールスポイント」が強調表示されます。

### ECへのワンタップ誘導
「在庫・詳細ページを開く」ボタンを配置し、ECサイト（デモURL）へ簡単に遷移できます。
