# 案件: Discord × Claude API連携 AI Bot開発

## 基本情報

| 項目 | 内容 |
|---|---|
| プラットフォーム | クラウドワークス |
| 案件URL | https://crowdworks.jp/public/jobs/13212376 |
| クライアント | hagiyama（レビュー51件） |
| 単価 | 50,000〜100,000円（固定） |
| 応募締切 | 2026-06-09 |
| 掲載日 | 2026-06-03 |
| 応募状況 | 87人応募・契約0人 |
| カテゴリ | AI・チャットボット開発 |

## 状態

- [ ] 提案文送付
- [ ] 受注確定
- [ ] 要件詳細確認（Discordサーバー情報・講座資料の受け取り）
- [ ] 実装完了
- [ ] テスト完了
- [ ] 納品
- [ ] 支払い確認
- [ ] レビュー獲得

## クライアント要件まとめ

### 必須機能
1. 指定チャンネルのみでBotが反応する
2. 受講生の質問 → Claude API → 回答をDiscordに返信
3. トーン・ルールをこちら側で指定できる
4. 講座資料・FAQ・回答テンプレを参照して回答
5. 回答末尾に「必要に応じて運営に確認してください」等の注意文
6. 質問・回答のログ保存
7. Googleスプレッドシートへの質問ログ自動保存
8. APIキー・Tokenの安全な管理
9. プロンプト・回答ルールを後から修正しやすい構成

### あると嬉しい機能（加点）
- Botメンション時のみ返信するモード
- AI回答不能時は「運営に確認してください」と返す
- NGワード・回答禁止設定
- 下書きモード（運営確認後に返信）
- 講座資料追加時にAIの回答に反映する仕組み
- API使用量・コスト確認機能

### クライアントが用意するもの
- Discordサーバー
- Claude APIキー
- 講座資料・FAQ・回答テンプレ・口調ルール

## 実装計画（Claude Codeで実装）

### 技術スタック
```
discord.py          # Discord Bot本体
anthropic           # Claude API SDK
google-auth + gspread  # Google Sheets連携
python-dotenv       # 環境変数管理
```

### アーキテクチャ
```
Discord（質問チャンネル）
    ↓ on_message イベント
discord.py Bot
    ↓ 質問テキスト + システムプロンプト（講座方針）
Claude API
    ↓ 生成回答
Discord（同チャンネルに返信）
    ↓ 非同期
Google Sheets（ログ記録）
```

### ファイル構成（予定）
```
discord_bot/
├── bot.py              # メインBot
├── claude_client.py    # Claude API呼び出し
├── sheets_logger.py    # Googleスプレッドシート記録
├── config/
│   ├── system_prompt.txt   # プロンプト（クライアントが編集可）
│   ├── rules.txt           # 回答ルール
│   └── forbidden.txt       # NGワードリスト
├── .env                # トークン類（gitignore）
├── requirements.txt
└── README.md           # 操作マニュアル
```

### 実装工数見積もり（Claude Code活用）
| タスク | 実装時間 |
|---|---|
| Bot基本構造・チャンネル指定 | 1h |
| Claude API連携・プロンプト設計 | 1h |
| Googleスプレッドシートログ | 1h |
| 設定ファイル化（プロンプト・ルール） | 0.5h |
| あると嬉しい機能（メンション・NGワード等） | 1h |
| テスト・動作確認 | 1h |
| README・マニュアル作成 | 0.5h |
| **合計** | **約6時間** |

→ 時給換算: 50,000÷6 ≈ **8,300円/時間**

## 提案文

→ `projects/active/20260605_discord_claude_bot_proposal.md` 参照

## 振り返り（完了後に記入）

- 良かった点:
- 改善点:
- 次回への活かし方:
