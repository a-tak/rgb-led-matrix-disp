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
* データベースの`Name`列に名言を入れる

## 特殊記法

* Nameに特定の文字を入れることで表示内容を動的に変更することができます。

### 記載例

```plaintext
Youtubeを始めて{0}日です;datecount:"2021/08/30"
```

* リプレースホルダは `{0}` と記載します(現状1個のみで{1},{2}は対応してない)
* セミコロン`;` の後に `変換タイプ`:`パラメーター` の形式で動的表示の方法を指定。

### 指定した日付から今日までの経過日数を表示する(datecount)

#### 変換タイプ

`datecount`

#### 説明

パラメーターで与えた日数から今日までの経過日数を表示します

#### 例

```plaintext
Youtubeを始めて{0}日です;datecount:"2021/08/30"
```

#### 結果

```plaintext
Youtubeを始めて256日です
```

## Node-redのインストール

Alexaで制御する場合はNode-Redが必要。

[AlexaからRaspberry Piを経由して家電を音声で操作する](https://www.zumid.net/entry/raspberry-pi-alexa-home-app/) を参考にしてください。

サンプルも入れています

 [flows.json](flows.json)

## 温度・湿度・気圧表示モジュール

### 使用部品

* 温湿度・気圧センサ AE-BME280

### 回路図

![](doc-image/circuit-diagram.jpg)

* 明るさセンサ(照度センサ) TSL2561も回路図にあるが使用していない

### 設定

* I2CをRasp Configで有効にする
* 関連モジュールインストールと設定
    ```bash
    sudo apt-get update
    sudo apt-get install i2c-tools
    sudo apt-get install python-smbus
    sudo pip3 install smbus2
    sudo chmod a+rw /dev/i2c-1
    ```
* 権限の設定
    ```bash
    sudo vim /etc/udev/rules.d/99-com.rules
    ```

    ```bash
    SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="066**6**"
    ```

## 参考

* [Raspberry Pi で LED時計を作ってみた](https://a-tak.com/blog/2017/02/raspberry-pi-led-clock/)
* [PythonとLED MatrixでLED発車標風な時計を作る](https://qiita.com/sousan/items/19425d5eac43786003a7)
* [Raspberry Pi3B+でRGB LEDmatirix電光掲示板の表示を自在に操る](https://qiita.com/shuto1441/items/4c691dd3af948cc19bdf)
* [AlexaからRaspberry Piを経由して家電を音声で操作する](https://www.zumid.net/entry/raspberry-pi-alexa-home-app/)
* [Raspberry Piで実行する](https://nodered.jp/docs/getting-started/raspberrypi)
* [SWITCHSCIENCE/BME280](https://github.com/SWITCHSCIENCE/BME280/blob/master/Python27/bme280_sample.py)