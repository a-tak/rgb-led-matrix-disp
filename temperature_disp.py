#!/usr/bin/env python3
# coding: UTF-8
# Display Temperature
# sudo python3 temperature_disp.py --led-rows=16 --led-brightness=40
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
from disp_abc import DispAbc
from collections import namedtuple
from temperature_mod import TemperatureSensor

class TemperatureDisp(DispAbc):
    u"""温度表示クラス
    """
    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.accepted_stop = False

    def execute(self):
        u"""温度表示開始
        スレッドをstartすると__call__が暗黙的に呼ばれる
        """
        logger.debug("Temperture Disp Start")
        
        sensor = TemperatureSensor() 

        offscreen_canvas = self.matrix.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/5x7.bdf")

        while not self.accepted_stop:
            value = sensor.get()
            textColor1 = graphics.Color(255, 100, 100)
            textColor2 = graphics.Color(100, 255, 100)
            textColor3 = graphics.Color(100, 100, 255)
            textColor4 = graphics.Color(100, 100, 100)
            
            disp_text1 = str(value.temp)[0:4] + " C"
            disp_text2 = str(value.hum)[0:4] + " %"
            disp_text3 = str(value.hpa)[0:4]
            disp_text4 = "hPa"
            
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, 2, 7, textColor1, disp_text1)
            len = graphics.DrawText(offscreen_canvas, font, 2, 15, textColor2, disp_text2)
            offscreen_canvas = self.matrix.matrix.SwapOnVSync(offscreen_canvas)

            time.sleep(3)

            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, 2, 7, textColor3, disp_text3)
            len = graphics.DrawText(offscreen_canvas, font, 16, 15, textColor4, disp_text4)
            offscreen_canvas = self.matrix.matrix.SwapOnVSync(offscreen_canvas)
            
            time.sleep(3)

    def stop(self):
        self.accepted_stop = True
     
# Main function
if __name__ == "__main__":
    matrix = Matrix()
    #processメソッドを一度呼ぶ必要がある
    if (not matrix.process()):
        matrix.print_help()
    disp_obj = TemperatureDisp(matrix)
    disp_obj.execute()

