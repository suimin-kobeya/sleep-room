"""index.html から各記事ページを作り直す。
使い方: python3 tools/build_pages.py
記事を足すときは PAGES に1行足す: (ファイル名, ビュー名, タイトル, 説明文, OG画像)
"""
import re
BASE = "https://suimin-kobeya.github.io/sleep-room/"
PAGES = [
    ("pillow.html", "pillow", "枕は「高さ」で選ぶ｜睡眠の小部屋",
     "【PR】枕選びで迷ったら、まずは高さから。仰向け・横向き、寝姿勢別のチェックポイントをパーソナル睡眠アドバイザーが解説します。",
     "pins/pillow-height.png"),
    ("winter-dry.html", "winter-dry", "冬の寝室、乾燥してない？｜睡眠の小部屋",
     "【PR】暖房の季節は寝室の湿度の数字が下がりやすくなります。温湿度計の置き場所と、加湿器を選ぶときのチェックポイントをパーソナル睡眠アドバイザーが解説します。",
     "pins/dry-1.png"),
    ("travel-light.html", "travel-light", "旅先・帰省の部屋、明るさを整える｜睡眠の小部屋",
     "【PR】旅先や帰省先の部屋は、光の入り方がいつもと違います。到着後の光の入り口の探し方と、アイマスクを選ぶときのチェックポイントをパーソナル睡眠アドバイザーが解説します。",
     "pins/travel-1.png"),
]
src = open("index.html", encoding="utf-8").read()
for fn, view, title, desc, img in PAGES:
    s = src
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, 1)
    s = re.sub(r'<meta name="description" content=".*?">',
               f'<link rel="canonical" href="{BASE}{fn}">\n<meta property="og:title" content="{title}">\n'
               f'<meta property="og:image" content="{BASE}{img}">\n<meta name="description" content="{desc}">', s, 1)
    # 他の記事の商品枠（アフィリエイトリンク）はこのページに残さない
    def keep(m):
        return m.group(0) if m.group(1) == f"view-{view}" else ""
    s = re.sub(r'(?s)(?<=<article id=")(view-[a-z-]+)(.*?)(\n    <section class="product".*?</section>)',
               lambda m: m.group(1)+m.group(2)+(m.group(3) if m.group(1)==f"view-{view}" else ""), s)
    s = s.replace("<body>", f'<body data-view="{view}">', 1)
    open(fn, "w", encoding="utf-8").write(s)
    print(fn)
