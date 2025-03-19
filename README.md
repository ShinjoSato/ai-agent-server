# 分身AIエージェント（サーバーサイド）

<div style="display: flex; justify-content: center;">
    <video controls src="https://github.com/user-attachments/assets/71b373b3-8df1-48ed-91ba-c99c4dd591bf" muted="true"></video>
</div>

## 概要

自分の代わりに仕事をこなすAIエージェントを実現するために開発し始めました。

今後も生成AIとの連携を増やしていき、より多くの仕事を任せられるようなエージェントを目指していきます。

## 機能

- ***質問内容を分析***

    ユーザーからの問いを理解し、適切な回答を作成します。

- ***合成音声として出力***

    回答を要約して、合成音声AIを使って自分の声で返答します。


## 使用技術

- バックエンド

    Python3

- AIツール

  |対話|検索|音声合成|AIエージェント|
  |:--|:--|:--|:--|
  |OpenAI|Perplexity|EvelenLabs|LangGraph|


## 開発環境の構築

- ```.env.example```ファイルをコピーして新たに```.env```を作成し、使用するAPIキーなどを入力してください。
- ```requirements.txt```に書かれているpipライブラリをインストールしてください。
- 実行ファイルは```main.py```です。
