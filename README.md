# OpenAI サンプル

## 使い方

.env というファイルをルートにおいてください

```
OPENAI_API_KEY=****************
```

- OpenAI API キー

## 必要なライブラリのインストール

pip の場合

```
pip install -r requirements.txt
```

Anaconda の場合

```
conda env create -f environment.yaml
```

# Assistant - Thread

```
python server_assistants.py
```

例では過去の会話を記憶するスレッドを利用している。
OpenAI ダッシュボードで Retrieval を on にしてファイルをアップロードするとそのファイルを参照して回答してくれるはず（もちろんプログラムからでもできる）

## 会話

index.html をブラウザで開いて文章を入力して送信

# AWS Lambda を利用

サーバーレスを利用して安く運用することができる

- レイヤーに必要なライブラリを zip に圧縮してアップロード
- 関数を作成して openai_aws.py のコードを貼り付けして保存してデプロイ
- 関数 URL を作成して CORS 設定でほかのドメインを許可する

## 会話

openai_aws.html をブラウザで開いて文章を入力して送信
