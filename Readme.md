# 先進モビリティ学（自動運転）2021

## 目標
* 視野角を工夫して解決するのではなく，画像からうまくラインを検出して走行する

## To do list
* ~~SSH接続でOpencvの画像を出力できるようにする．~~
* 画像からラインを検出するためのプログラムを書く.

## ディレクトリ構成
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

## SSH接続でのGUI出力について
[RasPi側の設定1](https://users.miraclelinux.com/support/?q=node/374)
[RasPI側の設定2](https://richarthurs.com/2019/01/20/raspberrypi-cv-setup/)
[VScodeの拡張機能](https://www.server-memo.net/memo/vscode/vscode_ssh.html)
[SSH接続の方法](https://qiita.com/SOutaHI/items/10befdc15b9b3a33fd5e)

### ラズパイ側の設定
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

### VScodeの拡張機能を使ったSSH接続
VScodeの拡張機能に`Remote Developement`がある．これを使うとSSH接続先PC内のフォルダをvscodeで開き，接続元PCで編集することができる．

1. 拡張機能で`Remote Developement`で検索してインストールする
2. vscodeの左側にリモート接続のアイコンが追加されるので選択する
3. `ssh targets`を選択し，`+`ボタンを選択後，指示に従ってIPアドレス，パスワードを入力
4. SSH接続先のフォルダがvscodeで開かれ，編集ができるようになる．また，コマンドも実行できる．