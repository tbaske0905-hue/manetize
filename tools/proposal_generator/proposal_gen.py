"""
提案文テンプレート生成ツール（API不要版）

使い方:
  python proposal_gen.py --category vba
  python proposal_gen.py --category scraping
  python proposal_gen.py --category automation
  python proposal_gen.py --list

案件の詳細に合わせた提案文は、出力されたテンプレを
Claude Code（チャット）に貼り付けてカスタマイズしてもらう。
"""

import argparse

TEMPLATES = {
    "vba": {
        "label": "Excel VBA・マクロ開発",
        "template": """
はじめまして。Excelの業務自動化を専門にしているエンジニアです。

ご依頼内容を拝見しました。{pain_point}のお悩み、よくあるケースで対応実績がございます。

VBAマクロで{solution}を実現することで、作業時間を大幅に短縮できます。
コードにはコメントを丁寧に記載しますので、納品後もご自身で修正しやすい形でお渡しします。

最短翌日納品が可能です。

一点確認させてください。現在お使いのExcelのバージョン（2016・2019・365など）を教えていただけますか？
""",
        "hints": {
            "pain_point": "手作業でのデータ入力・集計",
            "solution": "ボタン一つで自動処理",
        },
    },
    "scraping": {
        "label": "Webスクレイピング・データ収集",
        "template": """
はじめまして。Pythonを使ったWebスクレイピング・データ収集を専門にしているエンジニアです。

{target_site}からのデータ収集ですね。同様の案件を複数対応してきました。

Pythonで収集ツールを作成し、{output_format}形式で納品いたします。
定期実行が必要な場合もスケジューラー設定まで対応可能です。

最短2〜3日での納品を予定しています。

確認なのですが、収集したいデータの件数と、更新頻度（一度きり／定期実行）を教えていただけますか？
""",
        "hints": {
            "target_site": "対象サイト名",
            "output_format": "Excel・CSV",
        },
    },
    "automation": {
        "label": "業務自動化・Python開発",
        "template": """
はじめまして。業務自動化ツールの開発を専門にしているエンジニアです。

{task}の自動化ですね。Pythonで実現できます。

{approach}という形で実装し、操作マニュアルも合わせて納品します。
導入後のちょっとした修正も対応可能ですのでご安心ください。

納期は{deadline}を目安に動かせます。

現在の手作業の流れを簡単に教えていただけますか？より的確なご提案ができます。
""",
        "hints": {
            "task": "繰り返し作業",
            "approach": "GUIツール or コマンドラインスクリプト",
            "deadline": "3〜5営業日",
        },
    },
    "data": {
        "label": "データ整形・変換・クレンジング",
        "template": """
はじめまして。データ処理・変換を専門にしているエンジニアです。

{data_type}のデータ整形ですね。Pythonで一括処理するスクリプトを作成します。

{process}を自動化し、{output}の形で納品いたします。
データ量が多くても高速に処理できます。

最短翌日〜2日での納品が可能です。

サンプルデータを1〜2行分共有いただけますか？より正確な見積もりができます。
""",
        "hints": {
            "data_type": "Excel・CSV",
            "process": "重複削除・フォーマット統一・結合",
            "output": "Excel・CSV",
        },
    },
}


def list_templates():
    print("利用可能なカテゴリ:\n")
    for key, val in TEMPLATES.items():
        print(f"  --category {key}  →  {val['label']}")
    print("\n使い方: python proposal_gen.py --category vba")
    print("\n出力されたテンプレをClaude Code（チャット）に貼って案件詳細に合わせてもらってください")


def get_template(category: str):
    if category not in TEMPLATES:
        print(f"カテゴリ '{category}' が見つかりません。--list で確認してください")
        return

    t = TEMPLATES[category]
    print(f"\n【{t['label']}】提案文テンプレート\n")
    print("=" * 60)
    print(t["template"].strip())
    print("=" * 60)
    print("\n【{}を埋めるヒント】".format("{}"))
    for k, v in t["hints"].items():
        print(f"  {{{k}}} → 例: {v}")
    print("\n→ このテンプレとともに案件の詳細をClaude Codeに貼ると、すぐカスタム提案文を作ってもらえます")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="提案文テンプレート生成（API不要）")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--category", choices=list(TEMPLATES.keys()), help="案件カテゴリ")
    group.add_argument("--list", action="store_true", help="カテゴリ一覧を表示")
    args = parser.parse_args()

    if args.list:
        list_templates()
    else:
        get_template(args.category)
