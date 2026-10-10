// 楽天の商品検索APIで「名人の本棚」の商品を集めて data/products.json に書く（キーは office/.env.local から読むだけ・表示しない）
// 使い方（meijin-site フォルダで）: node tools/fetch_products.mjs
import { readFileSync, writeFileSync, mkdirSync } from "fs";
const env = {}; for (const l of readFileSync("../office/.env.local", "utf-8").split(/\r?\n/)) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim(); }
const ORIGIN = "https://ymaiworks-office.vercel.app"; // 楽天の Allowed websites に入っている Origin
const API = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260701";
const SHELF = [
  { shelf: "いま遊べるドラクエ", keyword: "ドラゴンクエストI&II HD-2D Switch", pick: 1 },
  { shelf: "いま遊べるドラクエ", keyword: "ドラゴンクエストIII そして伝説へ Switch", pick: 1 },
  { shelf: "いま遊べるドラクエ", keyword: "ドラゴンクエストV 天空の花嫁 ニンテンドーDS", pick: 1 },
  { shelf: "名人の書庫", keyword: "ドラゴンクエストV 天空の花嫁 公式ガイドブック", pick: 1 },
  { shelf: "名人の書庫", keyword: "ドラゴンクエストIII そして伝説へ 公式ガイドブック", pick: 1 },
  { shelf: "名人の書庫", keyword: "交響組曲 ドラゴンクエスト ベスト・セレクション ロト編 すぎやまこういち", pick: 1 },
  { shelf: "名人の部屋", keyword: "ドラゴンクエスト ミミック ティッシュカバー", pick: 1 },
  { shelf: "名人の部屋", keyword: "スマイルスライム ぬいぐるみ スライム", pick: 1 },
  { shelf: "名人の部屋", keyword: "ドラゴンクエスト メタリックモンスターズギャラリー はぐれメタル", pick: 1 },
];
const out = [];
for (const s of SHELF) {
  await new Promise((s) => setTimeout(s, 1500)); // 楽天は1秒に1回まで
  const url = `${API}?applicationId=${encodeURIComponent(env.RAKUTEN_APP_ID)}&keyword=${encodeURIComponent(s.keyword)}&hits=10&availability=1&sort=-reviewCount&imageFlag=1&format=json`;
  const r = await fetch(url, { headers: { Origin: ORIGIN, Referer: ORIGIN + "/", accessKey: env.RAKUTEN_ACCESS_KEY } });
  const j = await r.json().catch(() => ({}));
  if (r.status !== 200) { console.log("失敗", s.keyword, r.status, JSON.stringify(j).slice(0, 120)); continue; }
  const items = (j.Items ?? []).map((w) => w.Item ?? w).filter((it) => it?.itemName && it?.itemUrl);
  for (const it of items.slice(0, s.pick)) {
    out.push({ shelf: s.shelf, keyword: s.keyword, name: it.itemName, shop: it.shopName, price: it.itemPrice,
      image: (it.mediumImageUrls?.[0]?.imageUrl ?? it.mediumImageUrls?.[0] ?? "").toString().replace(/([?&])_ex=\d+x\d+/, "$1_ex=300x300"),
      itemUrl: it.itemUrl, reviewCount: it.reviewCount, reviewAverage: it.reviewAverage });
    console.log(s.shelf, "|", it.itemPrice + "円", "|", it.reviewCount + "件", "|", it.itemName.slice(0, 50));
  }
}
mkdirSync("data", { recursive: true });
writeFileSync("data/products.json", JSON.stringify({ fetchedAt: new Date().toISOString(), items: out }, null, 2));
console.log("保存", out.length, "件");
