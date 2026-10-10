# 懐かしゲーム名人の小言 公式ページ（1枚）

2026-10-10 作成。本人「名人の小言のホームページつくって、アフィリエイトとかコラボで収益できないかね」。

- **YM AI Works の本サイト（homepage）とは分ける**：本サイトは LINEヤフー広告の審査のため「自社サービスのサイト」として作ってあり、アフィリエイトを載せると審査が読めない（ホームページ企画.md）。
- 中身：名人の顔・登録ボタン・投稿時刻／第1話からの再生リスト埋め込み／最新の小言（公開済みの回）／名人の本棚（楽天）／お仕事・コラボの相談（メール）／アフィリエイトの表示（ステマ規制）と権利の断り書き。
- 静的な1枚（index.html）。公開先の案＝GitHub Pages（ymaiworks-ctrl）。

## 更新のしかた
```
node tools/fetch_videos.mjs      # 公開済みの回と再生リスト（monogatari/.env.local の鍵）
node tools/fetch_products.mjs    # 楽天の商品（office/.env.local の鍵・1.5秒間隔）
python tools/gen.py              # index.html を書き出す
```
- 楽天アフィリエイトID は `data/config.json` の `rakutenAffiliateId`。**空のあいだはリンクに報酬が付かない**。
- 価格は取得日時点の表示（ページに日付を出している）。古くなったら fetch_products をやり直す。
- 公式の画像（ゲーム画面・パッケージ以外のキャラ絵）は使わない。商品画像は楽天APIが返すものだけ。
