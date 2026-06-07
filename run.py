"""
manetize メインランナー（API不要版）

使い方:
  python run.py            # 全プラットフォームをスクレイピング
  python run.py --lancers  # Lancersのみ
  python run.py --cw       # クラウドワークスのみ
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from tools.scraper.lancers_scraper import scrape_all as lancers_scrape
from tools.scraper.crowdworks_scraper import scrape_all as cw_scrape

OUTPUT_DIR = ROOT / "output"

KEYWORDS_GOOD = [
    "python", "vba", "マクロ", "スクレイピング", "自動化", "excel",
    "スクリプト", "データ収集", "api", "bot", "ツール作成",
]
KEYWORDS_NG = [
    "デザイン", "イラスト", "動画編集", "写真", "ライティング",
    "翻訳", "経理", "営業", "sns運用",
]
MIN_PRICE = 3000  # 円以下は除外


def score_job(job: dict) -> int:
    """キーワードベースで案件をスコアリング"""
    title = (job.get("title") or "").lower()
    price_str = (job.get("price") or "").replace(",", "").replace("円", "")

    score = 0

    for kw in KEYWORDS_GOOD:
        if kw in title:
            score += 20

    for kw in KEYWORDS_NG:
        if kw in title:
            score -= 50

    # 単価チェック
    import re
    nums = re.findall(r"\d+", price_str)
    if nums:
        price = int(nums[0])
        if price >= 30000:
            score += 30
        elif price >= 10000:
            score += 15
        elif price < MIN_PRICE:
            score -= 30

    return score


def filter_jobs(jobs: list[dict]) -> list[dict]:
    """スコア0以上の案件を抽出してスコア順に並べる"""
    scored = [(score_job(j), j) for j in jobs]
    scored = [(s, j) for s, j in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"score": s, **j} for s, j in scored]


def save_report(jobs: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    # JSON保存
    json_path = OUTPUT_DIR / f"jobs_{ts}.json"
    json_path.write_text(json.dumps(jobs, ensure_ascii=False, indent=2))

    # Markdownレポート保存
    md_path = OUTPUT_DIR / f"report_{ts}.md"
    lines = [f"# 案件レポート {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"]
    lines.append(f"合計 {len(jobs)} 件\n\n---\n\n")

    for i, job in enumerate(jobs[:20], 1):  # 上位20件
        lines.append(f"## {i}. {job['title']}\n\n")
        lines.append(f"- **カテゴリ**: {job.get('category', '-')}\n")
        lines.append(f"- **単価**: {job.get('price', '不明')}\n")
        lines.append(f"- **締切**: {job.get('deadline', '不明')}\n")
        lines.append(f"- **スコア**: {job.get('score', '-')}点\n")
        lines.append(f"- **URL**: {job.get('url', '')}\n\n")
        lines.append("**→ 提案文が必要な場合はURLとタイトルをClaude Codeに貼ってください**\n\n---\n\n")

    md_path.write_text("".join(lines))
    return md_path


def main():
    parser = argparse.ArgumentParser(description="manetize — 案件スクレイピング")
    parser.add_argument("--lancers", action="store_true", help="Lancersのみ")
    parser.add_argument("--cw", action="store_true", help="クラウドワークスのみ")
    args = parser.parse_args()

    run_all = not args.lancers and not args.cw

    print("=" * 60)
    print("manetize — 案件収集スタート")
    print("=" * 60)

    all_jobs = []

    if run_all or args.lancers:
        print("\nLancers スクレイピング中...")
        all_jobs.extend(lancers_scrape())

    if run_all or args.cw:
        print("\nクラウドワークス スクレイピング中...")
        all_jobs.extend(cw_scrape())

    print(f"\n取得: {len(all_jobs)} 件")

    if not all_jobs:
        print("案件を取得できませんでした。ネット接続やサイト構造の変化を確認してください。")
        sys.exit(1)

    filtered = filter_jobs(all_jobs)
    print(f"フィルタ後: {len(filtered)} 件（スコア順）\n")

    report_path = save_report(filtered)

    print("=" * 60)
    print(f"レポート保存: {report_path}")
    print("=" * 60)
    print("\n【次のステップ】")
    print("1. レポートを開いて気になる案件のURLを確認")
    print("2. 案件の説明文をClaude Code（このチャット）に貼る")
    print("3. 「この案件の提案文を書いて」と伝えるだけ")


if __name__ == "__main__":
    main()
