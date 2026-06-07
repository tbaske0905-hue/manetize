# manetize — Claude Code 指示書

## プロジェクト概要

クラウドワークス・Lancers案件をClaude Codeで効率化してマネタイズするプロジェクト。

## ディレクトリ構成

```
manetize/
├── CLAUDE.md                  # この指示書
├── README.md                  # プロジェクト概要
├── docs/
│   ├── strategy.md            # マネタイズ戦略・方針
│   └── platforms.md           # プラットフォーム別メモ
├── projects/
│   ├── _template.md           # 案件管理テンプレート
│   ├── backlog.md             # 案件バックログ（未着手リスト）
│   └── active/                # 進行中案件（1ファイル1案件）
├── memos/                     # 調査メモ・気づき
├── tools/                     # 再利用可能なツール・スクリプト
│   ├── scraper/               # スクレイピング系
│   ├── vba_generator/         # VBA生成系
│   └── proposal_generator/    # 提案文生成系
└── deliverables/              # 納品物（.gitignore対象）
```

## 作業ルール

- 新規案件着手時は `projects/active/YYYYMMDD_案件名.md` を作成する
- 納品完了後は `active/` から `projects/done/` に移動し `backlog.md` のステータスを更新する
- 再利用できるコードは必ず `tools/` に保存する
- 調査メモは `memos/YYYYMMDD_テーマ.md` に残す

## よく使うコマンド

```bash
# 進行中案件を確認
ls projects/active/

# バックログ確認
cat projects/backlog.md

# ツール一覧
ls tools/
```

## 優先カテゴリ（単価・速度・量のバランス）

1. Excel VBA / マクロ開発（25,000円〜、実装1〜3h）
2. Webスクレイピング（10,000〜50,000円、実装2〜5h）
3. データ変換・自動化スクリプト（5,000〜20,000円、実装1〜2h）
4. 提案文・記事生成（量産型、文字単価1〜3円）
