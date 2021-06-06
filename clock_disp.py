#!/usr/bin/env python3
# coding: UTF-8
# Display a Clock
from disp_abc import DispAbc
from matrix import Matrix
from rgbmatrix import graphics
from datetime import datetime
import time
import threading
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class ClockDisp(DispAbc):
    u"""時計表示クラス
    """
    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.accepted_stop = False

    def execute(self):
        u"""時計表示開始
        スレッドをstartすると__call__が暗黙的に呼ばれる
        """
        logger.debug("ClockDisp Start")
        offscreen_canvas = self.matrix.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./fonts/6x13.bdf")
        textColor = graphics.Color(100, 100, 255)

        while not self.accepted_stop:
            d = datetime.now()
            h = (" " + str(d.hour))[-2:]
            #スペースを頭に着けて最後から2文字背取得。1-9時の間も真ん中に時計が表示されるようにする考慮
            my_text = h + ":" + d.strftime("%M")
            #logger.debug(my_text)
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, 2, 12, textColor, my_text)
 
            time.sleep(0.01)
            offscreen_canvas = self.matrix.matrix.SwapOnVSync(offscreen_canvas)

    def stop(self):
        self.accepted_stop = True
        
# Main function
if __name__ == "__main__":
    matrix = Matrix()
    #processメソッドを一度呼ぶ必要がある
    if (not matrix.process()):
        matrix.print_help()
    disp_obj = ClockDisp(matrix)
    disp_obj.execute()

