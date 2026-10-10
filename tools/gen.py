# -*- coding: utf-8 -*-
"""懐かしゲーム名人の小言 公式ページ（1枚）を index.html に書き出す。

使い方（meijin-site フォルダで）:
  node tools/fetch_videos.mjs      … 公開済みの回と再生リストを data/videos.json に
  node tools/fetch_products.mjs    … 名人の本棚（楽天）を data/products.json に
  python tools/gen.py              … index.html を作る

楽天アフィリエイトID は data/config.json の rakutenAffiliateId。空のあいだは普通のリンク（報酬なし）。
"""
import html
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
JST = timezone(timedelta(hours=9))
cfg_path = ROOT / "data" / "config.json"
cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
AFF = (cfg.get("rakutenAffiliateId") or "").strip()
CHANNEL = "https://www.youtube.com/@meijin_kogoto"
MAIL = "ymaiworks@gmail.com"

vids = json.loads((ROOT / "data/videos.json").read_text(encoding="utf-8"))
prods = json.loads((ROOT / "data/products.json").read_text(encoding="utf-8"))
e = html.escape


def aff(url: str) -> str:
    if not AFF:
        return url
    return f"https://hb.afl.rakuten.co.jp/hgc/{AFF}/?pc={quote(url, safe='')}&m={quote(url, safe='')}"


def short_name(n: str) -> str:
    for cut in ("【", "["):
        if n.startswith(cut) and "】" in n[:20]:
            n = n.split("】", 1)[1]
    return n[:48] + ("…" if len(n) > 48 else "")


# 全話の再生リスト
pl_all = next((p for p in vids["playlists"] if "全話" in p["title"]), None)
pl_games = [p for p in vids["playlists"] if "全話" not in p["title"]]
latest_ep = max((v["ep"] for v in vids["videos"]), default=0)

cards = []
for v in vids["videos"][:8]:
    t = v["title"]
    cards.append(f'''<a class="ep" href="https://www.youtube.com/shorts/{e(v["id"])}" target="_blank" rel="noopener">
  <img src="https://i.ytimg.com/vi/{e(v["id"])}/hqdefault.jpg" alt="" loading="lazy" width="216" height="384">
  <span class="ep-no">第{v["ep"]}話</span>
  <span class="ep-t">{e(t.split("【")[0])}</span>
</a>''')

seen, shelves = set(), {}
for p in prods["items"]:
    if p["itemUrl"] in seen:
        continue
    seen.add(p["itemUrl"])
    shelves.setdefault(p["shelf"], []).append(p)
shelf_html = []
for name, items in shelves.items():
    li = "".join(f'''<a class="item" href="{e(aff(p["itemUrl"]))}" target="_blank" rel="sponsored noopener">
  <img src="{e(p["image"])}" alt="" loading="lazy" width="150" height="150">
  <span class="item-n">{e(short_name(p["name"]))}</span>
  <span class="item-p">{int(p["price"]):,}円<small>（{e(p["shop"])}）</small></span>
</a>''' for p in items)
    shelf_html.append(f'<h3 class="shelf">{e(name)}</h3><div class="items">{li}</div>')
fetched = datetime.fromisoformat(prods["fetchedAt"].replace("Z", "+00:00")).astimezone(JST).strftime("%Y年%m月%d日")

game_links = "".join(f'<a class="pl" href="https://www.youtube.com/playlist?list={e(p["id"])}" target="_blank" rel="noopener">{e(p["title"])}<small>{p["count"]}話</small></a>' for p in pl_games)

page = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>懐かしゲーム名人の小言</title>
<meta name="description" content="懐かしゲームの小ネタ・裏技・豆知識を、名人が40秒で小言するYouTubeショートのチャンネル。毎日11時・15時・19時・21時に1話ずつ。">
<meta property="og:title" content="懐かしゲーム名人の小言">
<meta property="og:description" content="懐かしゲームの小ネタ・裏技を、名人が40秒で。毎日4話。">
<meta property="og:image" content="assets/ogp.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/meijin.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&family=M+PLUS+1p:wght@500;800&display=swap" rel="stylesheet">
<style>
:root{{--y:#ffe600;--k:#111;--r:#e8192c;--g:#666;--bg:#fffdf3;--line:#eee}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--k);font-family:"M PLUS 1p",system-ui,sans-serif;line-height:1.7;-webkit-text-size-adjust:100%}}
a{{color:inherit}}
.wrap{{max-width:960px;margin:0 auto;padding:0 16px}}
.pop{{font-family:"Mochiy Pop One",sans-serif;font-weight:400;letter-spacing:.01em}}
.pr{{background:var(--k);color:#fff;font-size:12px;text-align:center;padding:6px 16px}}
header.hero{{background:var(--y);border-bottom:6px solid var(--k)}}
.hero .wrap{{display:flex;gap:28px;align-items:center;padding-top:40px;padding-bottom:40px}}
.face{{width:180px;height:180px;flex:0 0 auto;border-radius:50%;border:6px solid var(--k);background:#fff;overflow:hidden;box-shadow:6px 6px 0 var(--k)}}
.face img{{width:100%;height:100%;object-fit:cover}}
h1{{font-size:clamp(30px,6vw,52px);line-height:1.2}}
h1 .mk{{background:linear-gradient(transparent 58%,#fff 58%);padding:0 6px}}
.lead{{font-weight:800;margin-top:10px;font-size:18px}}
.times{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.times span{{background:var(--k);color:var(--y);font-weight:800;border-radius:999px;padding:2px 14px;font-size:15px}}
.cta{{display:inline-block;margin-top:18px;background:var(--r);color:#fff;text-decoration:none;font-weight:800;font-size:18px;padding:12px 26px;border-radius:12px;border:3px solid var(--k);box-shadow:4px 4px 0 var(--k)}}
.cta:active{{transform:translate(2px,2px);box-shadow:2px 2px 0 var(--k)}}
section{{padding:44px 0;border-bottom:1px solid var(--line)}}
h2{{font-size:clamp(24px,4.5vw,32px);margin-bottom:6px}}
h2 small{{display:block;font-family:"M PLUS 1p",sans-serif;font-size:14px;color:var(--g);font-weight:500}}
.player{{position:relative;width:100%;max-width:360px;aspect-ratio:9/16;margin:18px auto 0;border:4px solid var(--k);border-radius:16px;overflow:hidden;background:#000;box-shadow:6px 6px 0 var(--y)}}
.player iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.pls{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:16px}}
.pl{{text-decoration:none;font-weight:800;border:3px solid var(--k);background:#fff;border-radius:999px;padding:6px 16px}}
.pl small{{margin-left:6px;color:var(--g);font-weight:500}}
.eps{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}}
.ep{{position:relative;display:block;text-decoration:none;border-radius:12px;overflow:hidden;border:3px solid var(--k);background:#000}}
.ep img{{display:block;width:100%;height:auto;aspect-ratio:9/16;object-fit:cover}}
.ep-no{{position:absolute;top:8px;left:8px;background:var(--y);font-weight:800;font-size:13px;padding:0 8px;border-radius:6px}}
.ep-t{{position:absolute;left:0;right:0;bottom:0;padding:22px 8px 8px;color:#fff;font-weight:800;font-size:13px;line-height:1.4;background:linear-gradient(transparent,rgba(0,0,0,.85))}}
.note{{font-size:13px;color:var(--g);margin-top:10px}}
.shelf{{font-family:"Mochiy Pop One",sans-serif;font-size:20px;margin:26px 0 10px;padding-left:10px;border-left:8px solid var(--y)}}
.items{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.item{{display:flex;flex-direction:column;text-decoration:none;background:#fff;border:2px solid var(--k);border-radius:12px;padding:10px}}
.item img{{width:100%;height:auto;aspect-ratio:1;object-fit:contain;background:#fff}}
.item-n{{font-weight:800;font-size:13px;line-height:1.45;margin-top:8px;flex:1}}
.item-p{{font-weight:800;color:var(--r);margin-top:6px}}
.item-p small{{display:block;color:var(--g);font-weight:500;font-size:11px}}
.collab{{background:var(--k);color:#fff;border-radius:18px;padding:26px;margin-top:16px}}
.collab ul{{margin:12px 0 0 1.2em}}
.collab .cta{{border-color:#fff;box-shadow:4px 4px 0 var(--y)}}
footer{{padding:30px 0 50px;font-size:12px;color:var(--g)}}
footer p+p{{margin-top:6px}}
@media (max-width:720px){{
  .hero .wrap{{flex-direction:column;text-align:center;gap:18px}}
  .times{{justify-content:center}}
  .face{{width:140px;height:140px}}
  .eps{{grid-template-columns:repeat(2,1fr)}}
  .items{{grid-template-columns:repeat(2,1fr)}}
}}
</style>
</head>
<body>
<div class="pr">当ページはアフィリエイト広告（楽天アフィリエイト）を利用しています</div>
<header class="hero"><div class="wrap">
  <div class="face"><img src="assets/meijin.png" alt="名人"></div>
  <div>
    <h1 class="pop">懐かしゲーム<br><span class="mk">名人の小言</span></h1>
    <p class="lead">あの頃のゲームの小ネタ・裏技・豆知識を、名人が40秒で小言します。</p>
    <div class="times"><span>毎日 11時</span><span>15時</span><span>19時</span><span>21時</span></div>
    <a class="cta" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">YouTubeで名人を登録する</a>
  </div>
</div></header>

<main>
<section><div class="wrap">
  <h2 class="pop">第1話から見る<small>いま第{latest_ep}話まで公開中。続けて見ると、だんだん名人になれます</small></h2>
  {f'<div class="player"><iframe src="https://www.youtube.com/embed/videoseries?list={e(pl_all["id"])}" title="名人の小言 全話" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>' if pl_all else ''}
  <div class="pls">{game_links}</div>
</div></section>

<section><div class="wrap">
  <h2 class="pop">最新の小言<small>新しい順</small></h2>
  <div class="eps">{"".join(cards)}</div>
</div></section>

<section><div class="wrap">
  <h2 class="pop">名人の本棚<small>小言に出てきたゲームを、いま遊ぶなら</small></h2>
  {"".join(shelf_html)}
  <p class="note">価格・在庫は{fetched}時点のものです。最新の情報は各ショップでご確認ください。リンク先は楽天市場です。</p>
</div></section>

<section><div class="wrap">
  <h2 class="pop">お仕事・コラボのご相談</h2>
  <div class="collab">
    <p>ゲーム・グッズ・レトロゲームショップ・書籍などのご紹介を承ります。</p>
    <ul>
      <li>名人の小言の形（40秒ショート）での紹介</li>
      <li>レトロゲームやシリーズの小ネタを使ったコラボ企画</li>
      <li>攻略本・サントラ・グッズのレビュー</li>
    </ul>
    <p style="margin-top:12px">毎日4話・第{latest_ep}話まで公開中。ドラクエ1・3・5から、FF・ロマサガ・ドラゴンボールなどへ広げていきます。</p>
    <a class="cta" href="mailto:{MAIL}?subject={quote('【名人の小言】お仕事のご相談')}">メールで相談する</a>
  </div>
</div></section>
</main>

<footer><div class="wrap">
  <p>運営：YM AI Works（雅 -miyabi-）</p>
  <p>当ページはアフィリエイト広告（楽天アフィリエイト）を利用しています。商品の購入により運営者に報酬が支払われることがあります。</p>
  <p>「ドラゴンクエスト」は株式会社スクウェア・エニックスの登録商標です。当チャンネル・当ページは非公式のファン作品で、各権利者とは関係ありません。イラストはすべて当チャンネルのオリジナルです。</p>
</div></footer>
</body>
</html>
'''
(ROOT / "index.html").write_text(page, encoding="utf-8")
print("index.html", len(page), "bytes / 回", len(cards), "/ 商品", len(seen), "/ アフィリエイトID", "あり" if AFF else "なし（報酬なしリンク）")
