# JAIST GO

JAIST（北陸先端科学技術大学院大学）の学生向けの、**おでかけ募集掲示板アプリ**です。

キャンパスは車がないと移動しづらい場所にあるため、「買い物に行きたいけど車がない」「温泉に行く人を集めたい」「駅まで乗せてほしい」といった募集を気軽に出し合える場所として作っています。あわせて、大学周辺のお店の口コミも共有できます。

---

## 主な機能

### 募集掲示板
- 「車募集」「遊び」のカテゴリで募集を投稿・一覧表示
- 行き先・集合場所・連絡手段などのキーワード検索、カテゴリでの絞り込み
- 募集の詳細ページで、Google マップ上に **集合場所から目的地までのルート（車）** を表示
- 自分が作成した募集の削除

### 口コミ
- 大学周辺のお店について、店名・星評価（1〜5）・自由記述で口コミを投稿
- 直近 30 日の口コミ件数ランキング（上位 5 店舗）

### アカウント
- ユーザー登録・ログイン・ログアウト
- 掲示板・口コミ・募集 API はログインが必要

---

## 技術構成

| 区分 | 使用技術 |
| --- | --- |
| 言語 | Python 3.11 |
| Web フレームワーク | Flask 3 |
| パッケージ管理 | uv（venv + pip でも可） |
| 地図 | Google Maps JavaScript API（Directions） |
| データ保存 | SQLite（地図の地点情報）、JSON ファイル（ユーザー・募集・口コミ） |
| フロントエンド | HTML / CSS / 素の JavaScript |

---

## ディレクトリ構成

```
JAIST-GO/
├── flaskr/
│   ├── __init__.py          # Flask アプリ本体の生成
│   ├── app.py               # 画面・API のルーティング、DB 用 CLI コマンド
│   ├── auth.py              # ユーザー登録・ログイン処理
│   ├── map.db               # 地点情報の SQLite データベース
│   ├── data/                # 実行時に自動生成（users / posts / reviews の JSON）
│   ├── static/demo/         # CSS・JavaScript
│   └── templates/           # HTML テンプレート
├── .env.template            # 環境変数のひな形
├── pyproject.toml           # 依存パッケージの定義（uv 用）
└── uv.lock
```

---

## セットアップ

### 1. リポジトリを取得

```bash
git clone https://github.com/fujita-miyako/JAIST-GO.git
cd JAIST-GO
```

### 2. 依存パッケージをインストール

**uv を使う場合（推奨）**

```bash
uv sync
```

**venv を使う場合**

```bash
python -m venv .venv
source .venv/bin/activate      # Windows は .venv\Scripts\activate
pip install flask python-dotenv
```

### 3. Google Maps API キーを設定

地図の表示には Google Maps API キーが必要です（各自で発行してください）。
`.env.template` をコピーして `.env` を作り、キーを書き込みます。

```bash
cp .env.template .env
```

```env
# .env
google_map_api_key=ここに自分のAPIキー
```

> `.env` は `.gitignore` 済みです。API キーはコミットしないでください。
> キーがなくても掲示板・口コミは動きますが、募集詳細の地図は表示されません。

### 4. データベースを準備

以降のコマンドはすべて **`flaskr/` ディレクトリ内** で実行します（DB ファイルを相対パスで参照しているため）。

```bash
cd flaskr
uv run flask --app app create-db       # テーブル作成
uv run flask --app app insert-sample   # サンプル地点の登録（任意）
uv run flask --app app show-data       # 中身の確認
```

venv の場合は先頭の `uv run` を外してください。

---

## 起動方法（デバッグモード）

```bash
cd flaskr
uv run flask --app app run --debug
```

venv の場合：

```bash
cd flaskr
flask --app app run --debug
# うまくいかない場合
python -m flask --app app run --debug
```

起動したらブラウザで http://127.0.0.1:5000 を開き、ユーザー登録 → ログインして使います。

---

## CLI コマンド一覧

| コマンド | 内容 |
| --- | --- |
| `flask --app app create-db` | `map_information` テーブルを作成 |
| `flask --app app insert-sample` | サンプル地点（東京駅など 3 件）を登録 |
| `flask --app app add-data` | 緯度・経度・場所名を対話形式で入力して 1 件追加 |
| `flask --app app show-data` | 登録済みの地点を一覧表示 |

---

## 画面・API 一覧

| URL | メソッド | 内容 | ログイン |
| --- | --- | --- | --- |
| `/` | GET / POST | 募集掲示板・口コミ（POST は口コミ投稿） | 必要 |
| `/posts/<id>` | GET | 募集の詳細 | 必要 |
| `/map/<id>` | GET | 地図表示（`dest_lat`, `dest_lng` を付けるとルート表示） | 不要 |
| `/register` | GET / POST | ユーザー登録 | 不要 |
| `/login` | GET / POST | ログイン | 不要 |
| `/logout` | POST | ログアウト | ― |
| `/api/posts` | GET | 募集一覧（`category`, `q` で絞り込み） | 必要 |
| `/api/posts` | POST | 募集を作成 | 必要 |
| `/api/posts/<id>` | GET | 募集を 1 件取得 | 必要 |
| `/api/posts/<id>` | DELETE | 募集を削除（作成者のみ） | 必要 |

---

## 開発メモ

- **データの保存先**：ユーザー・募集・口コミは `flaskr/data/` 以下の JSON ファイルに保存されます（初回書き込み時に自動作成）。地図の地点情報だけ SQLite（`map.db`）です。
- **パッケージの追加**（uv）：`uv add ライブラリ名`
- **本番運用前にやること**
  - `SECRET_KEY` が `flaskr/__init__.py` に直書きされているので、`.env` から読み込む形に変更する
  - デバッグモードを無効にして起動する
