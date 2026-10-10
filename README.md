# 懐かしゲーム名人の小言 公式ページ（1枚）

2026-10-10 作成。本人「名人の小言のホームページつくって、アフィリエイトとかコラボで収益できないかね」。

- **YM AI Works の本サイト（homepage）とは分ける**：本サイトは LINEヤフー広告の審査のため「自社サービスのサイト」として作ってあり、アフィリエイトを載せると審査が読めない（ホームページ企画.md）。
- 中身：名人の顔・登録ボタン・投稿時刻／第1話からの再生リスト埋め込み／最新の小言（公開済みの回）／名人の本棚（楽天）／お仕事・コラボの相談（メール）／アフィリエイトの表示（ステマ規制）と権利の断り書き。
- 静的な1枚（index.html）。公開先の案＝GitHub Pages（ymaiworks-ctrl）。

## 更新のしかた
```
node tools/fetch_videos.mjs      # 公開済みの回と再生リスト（monogatari/.env.local の鍵）
node tools/fetch_products.mjs    # 楽天の商品（office/.env.local の鍵・1.5秒間隔）
# （v1 の gen.py は廃止。いまのページは data/*.json をブラウザで読むので、データを更新して push するだけ）
```
- 楽天アフィリエイトID は `data/config.json` の `rakutenAffiliateId`。**空のあいだはリンクに報酬が付かない**。
- 価格は取得日時点の表示（ページに日付を出している）。古くなったら fetch_products をやり直す。
- 公式の画像（ゲーム画面・パッケージ以外のキャラ絵）は使わない。商品画像は楽天APIが返すものだけ。

## 2026-10-10 作り直し：レトロRPG風（ちぴの設計書）
- 見た目：黒地＋白の二重枠の「ウィンドウ」、DotGothic16、濃紺の背景、名人のドット絵（assets/meijin_dot.png＝meijin.png を48pxに縮めてニアレストで拡大）
- トップ：メッセージウィンドウ（1文字ずつ・タップで次へ）／コマンド（↑↓とEnterでも動く）／ステータス／最新の小言（埋め込み＋6話＋第1話から＋登録）
- 中身は data/site.json（セリフ・ステータス・自己紹介・フォームのURL）と data/videos.json。HTMLは触らずに増やせる
- 共通：assets/css/rpg.css・assets/js/rpg.js
- 残り4ページ（review/soubi/games/contact）は「じゅんびちゅう」の仮。順に作る
- **作品名は見た目に使わない（ロゴ・キャラ・音）**。文章とレビューの中では名前を出す
- **「愛用機材」とは書かない**（名人は架空なので、実際の使用を装う形になる）→「名人のおすすめ」
- 問い合わせフォーム：Googleフォーム/Formspree は本人のアカウントで作る → URL を data/site.json の formEmbedUrl に入れれば埋め込まれる。それまではメール
- 手元の確認：.claude/launch.json の「meijin-site」（http://127.0.0.1:8141/）

## 2026-10-10 公開・アプリ化
- 5ページ（index / review / soubi / games / contact）＋ data/*.json（site・reviews・soubi・games・videos・products・config）
- **増やし方**：レビュー＝data/reviews.json に1件足す／道具＝data/soubi.json／ゲーム＝data/games.json。HTMLは触らない
- 楽天リンクは assets/js/aff.js が data/config.json の ID を付けて作る（検索キーワード方式＝売り切れに強い）。Amazon は URL を入れるまで「じゅんびちゅう」
- 媒体資料の数字は data/videos.json の stats（`node tools/fetch_videos.mjs` で更新）
- **アプリとして入れられる（PWA）**：manifest.webmanifest・sw.js・assets/icon-192/512.png。Chrome/Edge の「アプリをインストール」で、デスクトップとスタートメニューにアイコンができる
