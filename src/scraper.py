import feedparser, json
from datetime import datetime

FEEDS = [
 "http://feeds.reuters.com/Reuters/worldNews",
 "http://feeds.bbci.co.uk/news/world/rss.xml"
]

OUT = "../data/raw/news.json"

data = []

for f in FEEDS:
    feed = feedparser.parse(f)
    for e in feed.entries:
        data.append({
            "title": e.title,
            "summary": getattr(e, "summary", ""),
            "source": f
        })

with open(OUT, "w") as f:
    json.dump({"ts": str(datetime.utcnow()), "articles": data}, f)

print(f"[+] {len(data)} noticias")
