#!/usr/bin/env python3
# coding: UTF-8
# Display a Meigen
# sudo python3 ./meigen_disp.py --led-rows=16 --led-brightness=40
from disp_abc import DispAbc
from matrix import Matrix
import time
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from logging import getLogger, StreamHandler, DEBUG
from notion_client import Client
import yaml
from datetime import datetime as dt

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class MeigenDisp(DispAbc):
    """名言表示クラス"""

    # テキストと関数を分割する文字
    FUNC_SEP = ';'
    # リプレースホルダの文字列
    REP_HOLDER = '{0}'
    # 変換タイプとパラメーターを分割する文字
    TYPE_SEP = ':'
    # 変換タイプ 日付カウント
    FUNC_DATE_COUNT = 'datecount'

    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.accepted_stop = False

    def imaged_text(self, text, fontfile, fontsize, color, scale_bias=4):
        font = ImageFont.truetype(fontfile, fontsize * scale_bias)
        image = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(image)
        w, h = draw.textsize(text, font=font)
        del draw
        image = Image.new('RGBA', (w, h))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=color)
        del draw
        return image.resize((w // scale_bias, h // scale_bias), Image.ANTIALIAS)

    def draw_text_to(self, target, position, text, fontfile, fontsize, color):
        image = self.imaged_text(text, fontfile, fontsize, color)
        target.paste(image, position, image)

    def select_color(self, threshold, color, destcolor='#FFFFFF'):
        mean = np.array(color).mean()
        if mean > threshold:
            # return (255, 255, 255)
            return (int(destcolor[1:3], 16), int(destcolor[3:5], 16), int(destcolor[5:7], 16))

        else:
            return (0, 0, 0)

    # 文字画像二値化
    def to_bin(self, img, w, h, color='#FFFFFF'):
        # 各画素値のr,g,bの平均を求める
        means = np.array([[img.getpixel((x, y)) for x in range(w)]
                         for y in range(h)]).mean(axis=2).reshape(w * h,)
        # ヒストグラムを作る
        hist = np.array([np.sum(means == i) for i in range(256)])
        max_v = 0
        threshold = 0
        # 0から255まで順に計算し、適切な閾値を求める
        # 閾値より大きい画素値をクラス１、小さい画素値をクラス２とする
        for th in range(256):
            n1 = sum(hist[:th])                                 # クラス１の個数
            m1 = np.dot(hist[:th], np.array(range(256))[:th])   # クラス１の値の平均
            n2 = sum(hist[th:])                                 # クラス２の個数
            m2 = np.dot(hist[th:], np.array(range(256))[th:])   # クラス２の値の平均
            if n1 == 0 or n2 == 0:
                v = 0
            else:
                # クラス間分散の分子を求める
                v = n1 * n2 * (m1 / n1 - m2 / n2) ** 2
            # クラス間分散の分子が最大となる閾値を更新していく
            if max_v < v:
                max_v = v
                threshold = th
        bin_img = Image.new('RGB', (w, h))
        np.array([[bin_img.putpixel((x, y), self.select_color(
            threshold, img.getpixel((x, y)), color)) for x in range(w)] for y in range(h)])
        return bin_img

    def get_text(self, str, width, separator=u"", col='#B5E61D'):
        image = Image.new("RGB", (width, 16))
        self.draw_text_to(image, (0, 0), separator + str,
                          'fonts/KH-Dot-Kodenmachou-16.ttf', 16, col)
        bin = self.to_bin(image, image.width, image.height, col)
        return bin

    def get_concat_h(self, im1, im2):
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    def replace_text(self, text):
        """テキスト内のリプレースホルダを置き換える"""
        # セミコロンで分割
        text_and_func = text.split(self.FUNC_SEP)

        # セミコロンがない、もしくは3つ以上の時は変換せずにもどる
        if len(text_and_func) ==1 or len(text_and_func) >= 3:
            return text

        text_body = text_and_func[0]
        func_and_param = text_and_func[1]
        
        # リプレースホルダがない場合はテキストをそのまま戻す
        if not (self.REP_HOLDER in text_body):
            return text_body

        # 変換タイプ名とパラメーターを分割
        type_and_param = text_and_func[1].split(self.TYPE_SEP)

        # 変換タイプとパラメーターが分割できない場合はテキストをそのまま戻す
        if len(type_and_param) == 1 or len(type_and_param) >= 3:
            return text_and_func[0]
        
        func_type = type_and_param[0]
        # ダブルクォーテーション外す
        func_param = type_and_param[1].replace('"','').strip()

        # 変換タイプ毎の処理
        result = ""
        if func_type == self.FUNC_DATE_COUNT:
            result = self.replace_datecount(text_body, func_param)
        else:
            # 該当する変換タイプがない時は変換せずに返す
            return text_body

        # 変換結果応答
        return result

    def replace_datecount(self, text, parameter):
        """テキスト内に日付カウントを埋め込む"""
        # 文字列から日付変換 & パラメーターが日付形式か?
        base_date = None
        try:
            base_date = dt.strptime(parameter, '%Y/%m/%d')
        except ValueError:
            # 日付に変換できないパラメーターの場合は変換せずに返す
            return text

        # 今日までの日数カウント
        daycount = (dt.now() - base_date).days

        # テキストに埋め込み
        result = text.replace(self.REP_HOLDER, str(daycount))

        # 変換結果応答
        return result

    def execute(self):
        """名言表示開始"""
        logger.debug("MeigenDisp Start")

        #設定読み込み
        yamlfile = "./setting.yaml"
        with open(yamlfile, "rt") as fp:
            text = fp.read()
        setting = yaml.safe_load(text)
        notion_token = setting["notion-token"]
        notion_db_id = setting["notion-db-id"]

        # Notionからデータ取得(一旦モード切替時のみ読み込むようにした)
        contents = []
        next_cursor = ""
        notion = Client(auth=notion_token)

        while next_cursor != None:
            # 初回と次ページがない時のクエリ
            if next_cursor == "" or next_cursor == None:
                pages = notion.databases.query(
                    **{
                        "database_id": notion_db_id,
                        "sorts": [
                            {
                                "timestamp": "last_edited_time",
                                "direction": "descending"
                            }
                        ]
                    }
                )
            else:
                # 次ページがある場合のクエリ 前のnext_cursorでもどってきたのをstart_cursorに指定する
                # NotionのAPIは秒間平均3リクエストなので間隔を開ける
                time.sleep(0.4)
                pages = notion.databases.query(
                    **{
                        "database_id": notion_db_id,
                        "start_cursor": next_cursor,
                        "sorts": [
                            {
                                "timestamp": "last_edited_time",
                                "direction": "descending"
                            }
                        ]
                    }
                )
            next_cursor = pages["next_cursor"]
            for result in pages["results"]:
                line = ""
                # 1レコードで複数に分かれる場合があるので1行に結合する
                for word in result["properties"]["Name"]["title"]:
                    line = line + word["text"]["content"]

                # 動的変換処理
                line = self.replace_text(line)
                contents.append(line)

        while True:
            # 名言表示ループ
            for item in contents:
                if self.accepted_stop:
                    break

                # 文字を画像化
                result = self.get_text(
                    item, len(item) * 16 + (16*2), u"", "#7777FF")

                # スクロール表示
                double_buffer = self.matrix.matrix.CreateFrameCanvas()
                img_width, img_height = result.size

                xpos = -32
                while True:
                    xpos += 1
                    if (xpos > img_width):
                        break

                    double_buffer.Clear()
                    double_buffer.SetImage(result, -xpos)
                    double_buffer = self.matrix.matrix.SwapOnVSync(double_buffer)
    
                    time.sleep(0.025)
                    if self.accepted_stop:
                        break
            if self.accepted_stop:
                break
            time.sleep(1)
    def stop(self):
        self.accepted_stop = True


if __name__ == "__main__":
    matrix = Matrix()
    # processメソッドを一度呼ぶ必要がある
    if (not matrix.process()):
        matrix.print_help()
    disp_obj = MeigenDisp(matrix)
    disp_obj.execute()
