#!/usr/bin/env python3
# coding: UTF-8
# 日付表示
from disp_abc import DispAbc
from matrix import Matrix
from rgbmatrix import graphics
from datetime import datetime
import time
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class DateDisp(DispAbc):
    u"""
    時計表示クラス
    """
    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.accepted_stop = False

    def execute(self):
        u"""
        時計表示開始
        """
        logger.debug("DateDisp Start")
        offscreen_canvas = self.matrix.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font1.LoadFont("fonts/5x7.bdf")
        textColor1 = graphics.Color(100, 200, 100)
        font2 = graphics.Font()
        font2.LoadFont("fonts/6x10.bdf")
        textColor2 = graphics.Color(50, 50, 200)

        while not self.accepted_stop:
            d = datetime.now()
            disp_text1 = d.strftime("%Y")
            disp_text2 = d.strftime("%m-%d")
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font1, 7, 6, textColor1, disp_text1)
            len = graphics.DrawText(offscreen_canvas, font2, 2, 16, textColor2, disp_text2)
            
            offscreen_canvas = self.matrix.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(0.01)

    def stop(self):
        self.accepted_stop = True

# Main function
if __name__ == "__main__":
    matrix = Matrix()
    # processメソッドを一度呼ぶ必要がある
    if (not matrix.process()):
        matrix.print_help()
    disp_obj = DateDisp(Matrix())
    disp_obj.execute()

