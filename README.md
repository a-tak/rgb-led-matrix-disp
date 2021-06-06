# rgb-led-matrix-disp

## 概要

[Raspberry Pi で LED時計を作ってみた](https://a-tak.com/blog/2017/02/raspberry-pi-led-clock/) で作成した[16x32 RGB LEDマトリックスパネル](http://www.amazon.co.jp/exec/obidos/ASIN/B0169UBW5G/website1-22/)制御アプリを再整理し、新たにNotionの特定のデータベースから拾い出したタイトルをスクロール表示する機能を追加した。


## 注意点

現状、rpi-rgb-led-matrixのPython用ライブラリの場所はソース内に直接記載している。

`matrix.py`の以下の部分。

```python
sys.path.append("/home/pi/rpi-rgb-led-matrix/bindings/python/rgbmatrix")
from rgbmatrix import RGBMatrix, RGBMatrixOptions
```

## 必要ライブラリ

```bash
sudo pip3 install pyyaml
sudo pip3 install notion-client
```

## LEDパネル制御ライブラリ

以下も必要。

[Controlling RGB LED display with Raspberry Pi GPIO](https://github.com/hzeller/rpi-rgb-led-matrix/)

[このあたり](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)を参考にPython用ライブラリのビルドが必要。

## フォント

以下からダウンロードし`fonts`ディレクトリを作成して入れてください。
* http://jikasei.me/font/kh-dotfont/
* https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/fonts

## setting.yamlの設定

|項目|内容|
|---|---|
|modefile-path|モード切替制御ファイルの置き場所。Node-Red等外部アプリから特定文字列を記載したmodeというファイルを置くことでLEDの表示を切り替えできる
|notion-token|Notionのトークンを設定する|
|notion-db-id|「名言」を取得してくるNotionのデータベースIDを設定する|

### 注意

modefile-pathに指定したディレクトリは権限777などにしないとPython側からmodeファイルを削除できないかもしれない

## Notion側設定

* インテグレーションをデータベースのShareに追加
* NotionトークンとデータベースIDをsetting.yamlにセット
* データベースに`meigen`という名称で名言を入れる

## Node-redのインストール

Alexaで制御する場合はNode-Redが必要。

[AlexaからRaspberry Piを経由して家電を音声で操作する](https://www.zumid.net/entry/raspberry-pi-alexa-home-app/) を参考にしてください。

サンプルも入れています

 [flows.json](flows.json)

## 参考

* [Raspberry Pi で LED時計を作ってみた](https://a-tak.com/blog/2017/02/raspberry-pi-led-clock/)
* [PythonとLED MatrixでLED発車標風な時計を作る](https://qiita.com/sousan/items/19425d5eac43786003a7)
* [Raspberry Pi3B+でRGB LEDmatirix電光掲示板の表示を自在に操る](https://qiita.com/shuto1441/items/4c691dd3af948cc19bdf)
* [AlexaからRaspberry Piを経由して家電を音声で操作する](https://www.zumid.net/entry/raspberry-pi-alexa-home-app/)
* [Raspberry Piで実行する](https://nodered.jp/docs/getting-started/raspberrypi)
