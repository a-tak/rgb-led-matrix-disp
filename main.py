#!/usr/bin/env python3
# coding: UTF-8
# RGB LED Matrix Main Module
from meigen_disp import MeigenDisp
from matrix import Matrix
from setting_controller import SettingController
from clock_disp import ClockDisp
from date_disp import DateDisp
from temperature_disp import TemperatureDisp
from mode import Mode
from datetime import datetime
import time
import threading
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
import traceback
import yaml

class Main():
    def __init__(self, *args, **kwargs):
        self.mode = Mode.CLOCK
        self.disp_thread = None
        self.disp_obj = None
        self.matrix = Matrix()
        #processメソッドを一度呼ぶ必要がある
        if (not self.matrix.process()):
            self.matrix.print_help()

    def main_loop(self):
        #設定読み込み
        yamlfile = "./setting.yaml"
        with open(yamlfile, "rt") as fp:
            text = fp.read()
        setting = yaml.safe_load(text)
        print("Setting Loading...")
        print(setting["modefile-path"])

        setting_thread =SettingController(setting["modefile-path"])
        setting_thread.start()

        self.mode = Mode.CLOCK
        self.switch_disp()

        while True:
            time.sleep(1)
            mode = setting_thread.get()
            if  mode is not None:
                logger.debug("detect mode changed.")
                self.mode = mode
                self.switch_disp()
    
    def switch_disp(self):
        self.stop_disp()
        if self.mode == Mode.CLOCK:
            self.stop_disp()
            self.disp_clock()
        elif self.mode == Mode.DATE:
            self.disp_obj = DateDisp(self.matrix)
            self.disp_start(self.disp_obj)
            time.sleep(4)
            self.stop_disp()
            self.disp_clock()
        elif self.mode == Mode.TEMP:
            self.disp_obj = TemperatureDisp(self.matrix)
            self.disp_start(self.disp_obj)
            time.sleep(12)
            self.stop_disp()
            self.disp_clock()
        elif self.mode == Mode.MEIGEN:
            self.disp_obj = MeigenDisp(self.matrix)
            self.disp_start(self.disp_obj)

    def disp_clock(self):
        self.disp_obj = ClockDisp(self.matrix)
        self.disp_start(self.disp_obj)
        self.mode = Mode.CLOCK

    def stop_disp(self):
        if self.disp_obj is not None:
            self.disp_obj.stop()
            self.disp_thread.join()

    def disp_start(self, disp_obj):
        self.disp_thread = threading.Thread(target=disp_obj.execute, name="disp")
        self.disp_thread.setDaemon(True)
        self.disp_thread.start()

# Main function
if __name__ == "__main__":
    try:
        main_obj = Main()
        main_obj.main_loop()
    except:
        logger.critical(traceback.format_exc())
        raise

