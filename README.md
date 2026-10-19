# はまこれ横浜 サイネージ表示ページ

背景画像（1280×720）の右側2枠に、はまこれ横浜の最新記事（画像＋タイトル）を表示するページです。

## 構成
- `index.html` … 表示ページ（全画面で拡大縮小。12秒ごとに2件ずつフェード切替、30分ごとにデータ再読込）
- `background.jpg` … 背景画像
- `feed.json` … 表示データ（初期値は10/19時点の記事。以降は自動更新）
- `scripts/fetch_feed.py` … RSSを取得して feed.json を作るスクリプト
- `.github/workflows/update-feed.yml` … 30分ごとに自動実行

## 公開手順（GitHub Pages）
1. GitHubで新規リポジトリを作成（Pagesを無料で使うにはPublic）
2. このフォルダの中身をすべてアップロード（`.github` フォルダも忘れずに）
3. Settings → Pages → Source を「Deploy from a branch」、Branch を `main` / `(root)` にして保存
4. Settings → Actions → General → Workflow permissions を「Read and write permissions」にして保存
5. Actions タブ → 「Update feed.json」→ Run workflow で一度手動実行し、feed.json が更新されることを確認
6. `https://<ユーザー名>.github.io/<リポジトリ名>/` を表示用ブラウザでF11（全画面）

## 運用メモ
- 取得に失敗しても feed.json は上書きされず、前回の表示が続きます。
- 表示端末側のブラウザは、画面スリープ解除とカーソル非表示（ページ側で対応済み）を設定してください。
- 位置・文字サイズの調整は `index.html` の `#slot1` / `#slot2` / `.title` を編集します。
- 記事の画像・タイトルは、はまこれ横浜の著作物です。サイネージでの利用は運営者へ事前確認のうえ、出典表記を入れてください。
