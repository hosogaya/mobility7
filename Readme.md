# 先進モビリティ学（自動運転）2021

# 目標
* 視野角を工夫して解決するのではなく，画像からうまくラインを検出して走行する

# To do list
* ~~SSH接続でOpencvの画像を出力できるようにする．~~
* 画像からラインを検出するためのプログラムを書く.

# ディレクトリ構成
```shell
.
├── Readme.md # これ
├── cpp # どうしても処理速度が出なかったらc++で書きます
└── python # pythonでの開発環境
    |── src # ソースファイル郡
    |   ├── __pycache__
    |   │   └── image_processing.cpython-37.pyc
    |   ├── image_processing.py #カメラと画像処理関係をまとめる
    |   └── main.py # 実行するファイル
    |
    └── Readme.md # pythonで開発したプログラムについての解説
```

# SSH接続でのGUI出力について
[RasPi側の設定1](https://users.miraclelinux.com/support/?q=node/374)
[RasPI側の設定2](https://richarthurs.com/2019/01/20/raspberrypi-cv-setup/)
[VScodeの拡張機能](https://www.server-memo.net/memo/vscode/vscode_ssh.html)
[SSH接続の方法](https://qiita.com/SOutaHI/items/10befdc15b9b3a33fd5e)

## ラズパイ側の設定
X 11 window forwarding機能を使用すると，sshで接続した先のホストPC(SSHサーバ)のGUIアプリケーションを接続元のホストPC(SSHクライアント)で使用することができる．

1. 接続先のホストPCにおいて，sshdの設定を変更する．
`vim`を使用して`/etc/ssh/sshd_config`を編集する．
```shell
$ vim /etc/ssh/sshd_config # ファイルをvimで開く
X11forwarding yes　# これを一番下に追加
```

2. 設定を下記コマンドで有効化する．
```shell
$ service sshd_restart
```

3. 接続元PCから接続する
```shell
$ ssh -X pi@"192.168.**.**" # IPアドレスをいれる
```

4. 下記のように入力するとvscodeが開くはず
```shell
code 
```

## VScodeの拡張機能を使ったSSH接続
VScodeの拡張機能に`Remote Developement`がある．これを使うとSSH接続先PC内のフォルダをvscodeで開き，接続元PCで編集することができる．

1. 拡張機能で`Remote Developement`で検索してインストールする
2. vscodeの左側にリモート接続のアイコンが追加されるので選択する
3. `ssh targets`を選択し，`+`ボタンを選択後，指示に従ってIPアドレス，パスワードを入力
4. SSH接続先のフォルダがvscodeで開かれ，編集ができるようになる．また，コマンドも実行できる．

# Pythonについてのメモ

## 勉強サイト
[Pythonの基本](https://qiita.com/TakesxiSximada/items/65f8c018d25c6b08df85) : 基本中の基本を学べそう．仮想環境のところは飛ばしてもOK
[オブジェクト指向1](https://qiita.com/kaitolucifer/items/926ed9bc08426ad8e835)：pythonやるならオブジェクト指向はわからないとということで．オブジェクト指向はプログラミングにおいて超重要な概念ですのでこの機会に．
[オブジェクト指向2](https://www.headboost.jp/python-objective-paradigm/)：上のはかなりしっかり書かれてそうな感じだったので，もう少し軽めのやつです．

## 命名規則
[参考ページ](https://qiita.com/naomi7325/items/4eb1d2a40277361e898b)

* クラス名：単語の最初だけ大文字（PascalCase）
* 変数：小文字とアンダースコア（snake_case)
* 定数：すべて大文字 (ALL_CAPS)

## タイマー割り込みの方法について
[参考ページ](https://qiita.com/miminashi/items/50a4f0906ab8f18b105d)

下のプログラムでは`task`を0.1秒間隔で呼び出す.
```python
import signal
import time

def task(arg1, arg2):
    print(time.time())

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, task) #第２引数に呼び出す関数
    signal.setitimer(signal.ITIMER_REAL, 0.1, 0.1) # 第２引数が一回目の実行までの時間，第３引数が２回目以降の実行間隔[秒]
    while True: pass #
```

# c++についてメモ
[OpenCVのインストール](https://swallow-incubate.com/archives/blog/20200709/)；ポイントは仮想メモリを増やしておくこと．インストールは2,3時間かかると考えて気長に待つ．

# ラズパイについてのメモ
* GPIOの入力範囲は`700 ~ 2300` [参考ページ](https://mickey-happygolucky.hatenablog.com/entry/2019/10/23/114711)