"""
クラウドワークス新着案件スクレイパー（Playwright版）
JavaScript必須サイトのためヘッドレスブラウザで取得する
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SEARCH_TARGETS = [
    {"label": "VBA・マクロ", "url": "https://crowdworks.jp/public/jobs/category/13?order=new"},
    {"label": "スクレイピング", "url": "https://crowdworks.jp/public/jobs/category/282?order=new"},
    {"label": "Python自動化", "url": "https://crowdworks.jp/public/jobs/search?search%5Bkeywords%5D=Python+%E8%87%AA%E5%8B%95%E5%8C%96&order=new"},
    {"label": "AI・自動化ツール", "url": "https://crowdworks.jp/public/jobs/category/283?order=new"},
]

OUTPUT_DIR = Path(__file__).parent / "output"


def fetch_jobs(page, url: str, label: str) -> list[dict]:
    try:
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception as e:
        print(f"[ERROR] {label}: {e}")
        return []

    soup = BeautifulSoup(page.content(), "html.parser")
    jobs = []

    for card in soup.select("[class*='_root_b2jur']"):
        try:
            # タイトルとURL
            title_el = card.select_one("[class*='_itemTitle_']")
            link_el = card.select_one(f"a[href*='/public/jobs/']")

            if not title_el or not link_el:
                continue

            href = link_el.get("href", "")
            if not re.search(r"/public/jobs/\d+", href):
                continue

            full_url = "https://crowdworks.jp" + href if href.startswith("/") else href

            # 単価
            price_el = card.select_one("[class*='_amountPc_']")
            price = price_el.get_text(strip=True) if price_el else "要相談"

            # 締切
            deadline_el = card.select_one("[class*='_absoluteDate_']")
            deadline = deadline_el.get_text(strip=True) if deadline_el else ""

            jobs.append({
                "category": label,
                "title": title_el.get_text(strip=True),
                "url": full_url,
                "price": price,
                "deadline": deadline,
                "scraped_at": datetime.now().isoformat(),
            })
        except Exception:
            continue

    return jobs


def scrape_all() -> list[dict]:
    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )

        for target in SEARCH_TARGETS:
            print(f"取得中: {target['label']} ...")
            jobs = fetch_jobs(page, target["url"], target["label"])
            print(f"  → {len(jobs)} 件取得")
            all_jobs.extend(jobs)
            time.sleep(2)

        browser.close()

    return all_jobs


def save_results(jobs: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = OUTPUT_DIR / f"crowdworks_{ts}.json"
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
