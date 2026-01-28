# app.py
# 起動: streamlit run app.py
# products.csv と同じフォルダに置いてください

from __future__ import annotations

import pandas as pd
import streamlit as st

APP_TITLE = "CAGUUU 接客サポート"
CSV_PATH = "products.csv"

# ====== アクセシビリティ重視CSS（文字＆ボタンを強制的に大きく）======
ACCESSIBLE_CSS = """
<style>
/* 全体フォントを大きく */
html, body, [class*="css"]  {
  font-size: 20px !important; /* 20px以上 */
}

/* 見出しを大きく */
h1 { font-size: 34px !important; }
h2 { font-size: 28px !important; }
h3 { font-size: 24px !important; }

/* Streamlitボタンを大きく（高さ50px以上） */
.stButton > button {
  min-height: 56px !important;
  font-size: 22px !important;
  font-weight: 700 !important;
  width: 100% !important;
  border-radius: 14px !important;
  border: 2px solid #0b3d2e22;
}

/* 入力欄も大きく */
.stTextInput input {
  min-height: 56px !important;
  font-size: 22px !important;
}

/* カード風の枠 */
.cag-card {
  border: 2px solid #11111122;
  border-radius: 16px;
  padding: 14px 14px;
  margin: 10px 0;
  background: #ffffff;
}

/* 重要トークは赤＆太字 */
.cag-sales {
  color: #b00020;
  font-weight: 800;
}

/* ECリンクボタン（大きい） */
a.cag-ec-btn {
  display: block;
  width: 100%;
  text-align: center;
  background: #0b6b3a;          /* 濃い緑（アクション） */
  color: white !important;
  padding: 16px 14px;
  border-radius: 16px;
  font-size: 24px;
  font-weight: 800;
  text-decoration: none !important;
  border: 2px solid #064225;
}
a.cag-ec-btn:active { transform: scale(0.99); }

/* 画像を見やすく */
img.cag-thumb {
  border-radius: 14px;
  border: 2px solid #11111122;
}

/* バリエーション情報（補足）のデザイン */
.cag-variation {
  font-size: 18px !important;  /* 商品名より少し小さく */
  color: #555555;              /* 真っ黒ではなく濃いグレー */
  font-weight: 500;
  margin-top: -10px;           /* 商品名との距離を詰める */
  margin-bottom: 8px;
  background-color: #f0f2f6;   /* 薄い背景色で区分け */
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;       /* 文字の長さだけ背景をつける */
}
</style>
"""

CATEGORY_EMOJI = {
    "全商品": "🌏",
    "ベッド": "🛏️",
    "ソファ": "🛋️",
    "テーブル": "📚",
    "チェア": "🪑",
    "収納": "🧺",
    "デスク": "💻",
    "その他": "🎲",
    "照明": "💡",

}

def load_products(csv_path: str) -> pd.DataFrame:
    # variation_text を追加
    df = pd.read_csv(csv_path, dtype={"category": str, "product_name": str, "variation_text": str, "sales_point": str, "ec_url": str, "image_url": str})
    # priceは数字/文字どちらでも来る想定
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
    # 欠損対策
    for col in ["category", "product_name", "variation_text", "sales_point", "ec_url", "image_url"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)
    return df

def yen(n: int) -> str:
    # 「¥120,000」形式
    return f"¥{n:,}"

def init_state(categories: list[str]):
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = categories[0] if categories else "全て"
    if "selected_product_idx" not in st.session_state:
        st.session_state.selected_product_idx = None

def render_header():
    st.markdown(ACCESSIBLE_CSS, unsafe_allow_html=True)
    st.markdown(f"# {APP_TITLE}")
    st.caption("※接客中に片手で操作できる、商品トーク表示＆EC誘導ツール")

def render_category_switch(categories: list[str]):
    st.markdown("## カテゴリ")
    cols = st.columns(len(categories)) if categories else [st]
    for i, cat in enumerate(categories):
        emoji = CATEGORY_EMOJI.get(cat, "📦")
        label = f"{emoji} {cat}"
        # どのボタンが押されたかを明確にするため、選択中は文言を少し変える
        if cat == st.session_state.selected_category:
            label = f"✅ {label}"

        if cols[i].button(label, key=f"cat_btn_{cat}"):
            st.session_state.selected_category = cat
            st.session_state.selected_product_idx = None

def render_search_box():
    st.markdown("## 商品を探す（文字入力が面倒なら不要）")
    q = st.text_input("商品名で検索", value="", placeholder="例：ソファ / ベッド / 昇降", label_visibility="visible")
    return q.strip()

def render_product_grid(df: pd.DataFrame):
    st.markdown("## 商品一覧（タップして詳細）")

    if df.empty:
        st.info("該当する商品がありません。カテゴリや検索条件を変えてください。")
        return

    # 1商品 = 1カード（モバイルで押しやすく）
    for idx, row in df.reset_index(drop=True).iterrows():
        with st.container():
            st.markdown('<div class="cag-card">', unsafe_allow_html=True)

            left, right = st.columns([1, 2], vertical_alignment="center")
            with left:
                st.image(row["image_url"], width=140, caption="", output_format="auto")
            with right:
                st.markdown(f"### {row['product_name']}")
                
                # バリエーションがある場合のみ表示
                if row['variation_text'] and row['variation_text'].strip():
                    st.markdown(f'<div class="cag-variation">{row["variation_text"]}</div>', unsafe_allow_html=True)
                
                st.markdown(f"**通常税込価格：{yen(int(row['price']))}**")

            if st.button("詳細・トークを見る", key=f"detail_{idx}"):
                st.session_state.selected_product_idx = idx

            # 詳細は押されたカードだけ展開（画面が散らからない）
            if st.session_state.selected_product_idx == idx:
                render_detail_view(row)

            st.markdown("</div>", unsafe_allow_html=True)

def render_detail_view(row: pd.Series):
    # sales_point を最優先（H3で強調）
    st.markdown("### セールスポイント（接客トーク）")
    # 赤字＋太字で視認性UP
    points = row["sales_point"].replace("\\n", "<br>").replace("\n", "<br>")
    st.markdown(f'<div class="cag-sales">{points}</div>', unsafe_allow_html=True)

    st.markdown("#### ")
    # 巨大リンクボタン（ECへ）
    ec_url = row["ec_url"].strip()
    if ec_url:
        st.markdown(
            f'<a class="cag-ec-btn" href="{ec_url}" target="_blank" rel="noopener noreferrer">🌐 納期・詳細ページを開く（EC）</a>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("ECページURLが設定されていません（ec_url）。")

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")

    render_header()

    # CSV読み込み
    try:
        df_all = load_products(CSV_PATH)
    except FileNotFoundError:
        st.error(f"'{CSV_PATH}' が見つかりません。先に data_generator.py を実行して products.csv を作成してください。")
        st.stop()
    except Exception as e:
        st.error(f"CSVの読み込みに失敗しました: {e}")
        st.stop()

    # カテゴリ一覧（上部スイッチ用）
    categories = sorted([c for c in df_all["category"].unique().tolist() if c.strip()])
    categories.insert(0, "全商品")  # ← これを追加（リストの先頭に入れる）

    init_state(categories)

    # 上部：カテゴリボタン
    if categories:
        render_category_switch(categories)
    else:
        st.warning("category が見つかりません（products.csv を確認してください）。")

    # 検索（任意）
    query = render_search_box()

    # フィルタ適用
    df = df_all.copy()
    
    # 検索ワードがあるなら、カテゴリボタンを無視して「全商品」から探す
    if query:
        df = df[df["product_name"].str.contains(query, case=False, na=False)]
        # ユーザーに分かりやすくメッセージを出す
        if not df.empty:
            st.success(f"全カテゴリから 「{query}」 を検索しました")
            
    # 検索ワードがない時だけ、カテゴリボタンで絞り込む
    elif st.session_state.selected_category and st.session_state.selected_category != "全商品":
        df = df[df["category"] == st.session_state.selected_category]

    # 表示順は価格ではなく名前（現場で探しやすい）
    df = df.sort_values(by=["product_name"], ascending=True)

    render_product_grid(df)

if __name__ == "__main__":
    main()
