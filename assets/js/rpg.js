// 名人の小言 — 共通の動き（メッセージを1文字ずつ・コマンドのカーソル・データの読み込み）
const RPG = {
  async json(path) {
    const r = await fetch(path, { cache: "no-cache" });
    if (!r.ok) throw new Error(path + " " + r.status);
    return r.json();
  },

  /** メッセージウィンドウ：lines を1文字ずつ。タップで次の文へ（打ち終わっていなければ一気に表示） */
  typewriter(el, lines, speed = 55) {
    const body = el.querySelector(".text");
    let i = 0, timer = null, full = "";
    const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const show = (n) => {
      full = lines[n]; el.classList.remove("done"); body.textContent = "";
      if (reduce) { body.textContent = full; el.classList.add("done"); return; }
      let k = 0;
      clearInterval(timer);
      timer = setInterval(() => {
        body.textContent = full.slice(0, ++k);
        if (k >= full.length) { clearInterval(timer); el.classList.add("done"); }
      }, speed);
    };
    const next = () => {
      if (!el.classList.contains("done")) { clearInterval(timer); body.textContent = full; el.classList.add("done"); return; }
      if (i < lines.length - 1) show(++i);
    };
    el.addEventListener("click", next);
    el.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); next(); } });
    show(0);
  },

  /** コマンドウィンドウ：↑↓でカーソル移動、Enterで決定 */
  commandMenu(el) {
    const items = [...el.querySelectorAll("a")];
    let at = 0;
    const mark = (n) => { items.forEach((a, k) => a.classList.toggle("on", k === n)); at = n; };
    items.forEach((a, k) => { a.addEventListener("mouseenter", () => mark(k)); a.addEventListener("focus", () => mark(k)); });
    el.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); items[(at + 1) % items.length].focus(); }
      if (e.key === "ArrowUp") { e.preventDefault(); items[(at - 1 + items.length) % items.length].focus(); }
    });
    mark(0);
  },

  esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); },
};
