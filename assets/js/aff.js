// アフィリエイトリンクを作る（IDは data/config.json）。空なら普通のリンク
const AFF = {
  cfg: null,
  async load() { if (!this.cfg) this.cfg = await RPG.json("data/config.json").catch(() => ({})); return this.cfg; },
  rakutenSearch(keyword) {
    const url = "https://search.rakuten.co.jp/search/mall/" + encodeURIComponent(keyword) + "/";
    const id = (this.cfg?.rakutenAffiliateId || "").trim();
    return id ? `https://hb.afl.rakuten.co.jp/hgc/${id}/?pc=${encodeURIComponent(url)}&m=${encodeURIComponent(url)}` : url;
  },
  rakutenItem(itemUrl) {
    const id = (this.cfg?.rakutenAffiliateId || "").trim();
    return id ? `https://hb.afl.rakuten.co.jp/hgc/${id}/?pc=${encodeURIComponent(itemUrl)}&m=${encodeURIComponent(itemUrl)}` : itemUrl;
  },
  /** Amazon の検索リンク（タグは data/config.json の amazonTag）。タグが無ければ空＝ボタンを出さない */
  amazonSearch(keyword) {
    const tag = (this.cfg?.amazonTag || "").trim();
    if (!tag || !keyword) return "";
    return "https://www.amazon.co.jp/s?k=" + encodeURIComponent(keyword) + "&tag=" + encodeURIComponent(tag);
  },
  /** ボタン2つ（楽天・Amazon）。Amazon は URL が無いうちは「じゅんびちゅう」 */
  buttons(links) {
    const r = links.rakuten ? `<a class="btn" href="${RPG.esc(this.rakutenSearch(links.rakuten))}" target="_blank" rel="sponsored noopener">▶ 楽天でさがす</a>` : "";
    const am = links.amazon || this.amazonSearch(links.amazonKeyword || links.rakuten);
    const a = am
      ? `<a class="btn" href="${RPG.esc(am)}" target="_blank" rel="sponsored noopener">▶ Amazonでさがす</a>`
      : `<a class="btn" aria-disabled="true">Amazon（じゅんびちゅう）</a>`;
    return `<div class="rv-shop">${r}${a}</div>`;
  },
};
