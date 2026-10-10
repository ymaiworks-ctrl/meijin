// 公開済みの回（新しい順）と再生リストを data/videos.json に書く（monogatari/.env.local の鍵を読むだけ）
import { readFileSync, writeFileSync } from "fs";
const env = {}; for (const l of readFileSync("../monogatari/.env.local", "utf-8").split(/\r?\n/)) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim(); }
const tok = await fetch("https://oauth2.googleapis.com/token", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: new URLSearchParams({ client_id: env.YOUTUBE_CLIENT_ID, client_secret: env.YOUTUBE_CLIENT_SECRET, refresh_token: env.YOUTUBE_REFRESH_TOKEN, grant_type: "refresh_token" }) }).then((r) => r.json());
const H = { Authorization: `Bearer ${tok.access_token}` }; const API = "https://www.googleapis.com/youtube/v3";
const ch = await fetch(`${API}/channels?part=contentDetails,statistics&mine=true`, { headers: H }).then((r) => r.json());
const up = ch.items[0].contentDetails.relatedPlaylists.uploads;
const pl = await fetch(`${API}/playlistItems?part=contentDetails&maxResults=50&playlistId=${up}`, { headers: H }).then((r) => r.json());
const ids = pl.items.map((i) => i.contentDetails.videoId).join(",");
const v = await fetch(`${API}/videos?part=snippet,status,statistics&id=${ids}`, { headers: H }).then((r) => r.json());
const videos = v.items.filter((x) => x.status.privacyStatus === "public" && /第\d+話/.test(x.snippet.title))
  .map((x) => ({ id: x.id, title: x.snippet.title.replace(/\s*#shorts/i, ""), publishedAt: x.snippet.publishedAt, views: Number(x.statistics.viewCount ?? 0),
    ep: Number((x.snippet.title.match(/第(\d+)話/) ?? [])[1] ?? 0) }))
  .sort((a, b) => b.ep - a.ep);
const lists = await fetch(`${API}/playlists?part=snippet,contentDetails&mine=true&maxResults=20`, { headers: H }).then((r) => r.json());
const playlists = lists.items.map((p) => ({ id: p.id, title: p.snippet.title, count: p.contentDetails.itemCount }));
const st = ch.items[0].statistics ?? {};
const stats = { subscribers: Number(st.subscriberCount ?? 0), views: Number(st.viewCount ?? 0),
  episodes: videos.length, totalShortViews: videos.reduce((a, x) => a + x.views, 0) };
writeFileSync("data/videos.json", JSON.stringify({ fetchedAt: new Date().toISOString(), channelId: ch.items[0].id, stats, videos, playlists }, null, 2));
console.log("公開済み", videos.length, "本 / 再生リスト", playlists.length);
