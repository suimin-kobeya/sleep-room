"""楽天の商品URLからアフィリエイトリンクを作る（API不要）。
使い方: python3 tools/rakuten_link.py <楽天の商品URL>
"""
import sys
from urllib.parse import quote

AFFILIATE_ID = "590d288e.52f06b5f.590d288f.8e206090"  # 楽天アフィリエイトの公開リンクに含まれるID


def make(url: str) -> str:
    return f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={quote(url, safe='')}"


if __name__ == "__main__":
    print(make(sys.argv[1]))
