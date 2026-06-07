"""
Lancers新着案件スクレイパー
対象カテゴリ: VBA, スクレイピング, Python自動化, Excel自動化
"""

import json
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SEARCH_TARGETS = [
    {"label": "VBA・マクロ", "url": "https://www.lancers.jp/work/search/system/vba"},
    {"label": "スクレイピング", "url": "https://www.lancers.jp/work/search/system/scraping"},
    {"label": "Python自動化", "url": "https://www.lancers.jp/work/search?keyword=Python+%E8%87%AA%E5%8B%95%E5%8C%96&open=1"},
    {"label": "Excel自動化", "url": "https://www.lancers.jp/work/search?keyword=Excel+%E8%87%AA%E5%8B%95%E5%8C%96&open=1"},
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

OUTPUT_DIR = Path(__file__).parent / "output"


def fetch_jobs(url: str, label: str) -> list[dict]:
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] {label}: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    jobs = []

    for card in soup.select(".p-search-job-media"):
        try:
            title_el = card.select_one('a[href*="/work/detail/"]')
            price_el = card.select_one(".p-search-job-media__price")

            if not title_el:
                continue

            jobs.append({
                "category": label,
                "title": title_el.get_text(strip=True),
                "url": "https://www.lancers.jp" + title_el.get("href", ""),
                "price": price_el.get_text(strip=True) if price_el else "不明",
                "deadline": "",
                "scraped_at": datetime.now().isoformat(),
            })
        except Exception:
            continue

    return jobs


def scrape_all() -> list[dict]:
    all_jobs = []
    for target in SEARCH_TARGETS:
        print(f"取得中: {target['label']} ...")
        jobs = fetch_jobs(target["url"], target["label"])
        print(f"  → {len(jobs)} 件取得")
        all_jobs.extend(jobs)
        time.sleep(2)
    return all_jobs


def save_results(jobs: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = OUTPUT_DIR / f"lancers_{ts}.json"
    out_path.write_text(json.dumps(jobs, ensure_ascii=False, indent=2))
    print(f"保存: {out_path}")
    return out_path


if __name__ == "__main__":
    jobs = scrape_all()
    if jobs:
        save_results(jobs)
        print(f"\n合計 {len(jobs)} 件の案件を取得しました")
    else:
        print("案件を取得できませんでした")
