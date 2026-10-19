#!/usr/bin/env python3
"""はまこれ横浜のRSSを取得し、タイトル・リンク・画像を feed.json に書き出す。
取得や解析に失敗した場合は既存の feed.json を上書きしない（前回データを保持）。"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED_URL = "https://hamakore.yokohama/feed"
OUT = Path(__file__).resolve().parent.parent / "feed.json"
MAX_ITEMS = 10
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}
IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)


def first_image(item):
    html = item.findtext("content:encoded", default="", namespaces=NS)
    m = IMG_RE.search(html)
    return m.group(1) if m else ""


def main():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "hamakore-signage/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())

    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        image = first_image(it)
        if not (title and image):
            continue
        try:
            date = parsedate_to_datetime(it.findtext("pubDate")).isoformat()
        except Exception:
            date = ""
        items.append({"title": title, "link": link, "image": image, "date": date})
        if len(items) >= MAX_ITEMS:
            break

    if len(items) < 2:
        print("記事が2件未満のため feed.json を更新しません", file=sys.stderr)
        return 1

    OUT.write_text(json.dumps({"source": FEED_URL, "items": items}, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"{len(items)}件を書き出しました")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # ネットワーク障害等でも既存データは残す
        print(f"取得失敗: {e}", file=sys.stderr)
        sys.exit(0)
