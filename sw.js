// 名人の小言：アプリとして入れるための最小の service worker（ページは毎回ネットから取り、取れないときだけ控えを出す）
const CACHE = "meijin-v2";
const CORE = ["./", "index.html", "review.html", "soubi.html", "games.html", "contact.html", "assets/css/rpg.css", "assets/js/rpg.js", "assets/js/aff.js", "assets/meijin_dot.png", "assets/icon-192.png"];
self.addEventListener("install", (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", (e) => { e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  e.respondWith(fetch(e.request).then((r) => { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request)));
});
