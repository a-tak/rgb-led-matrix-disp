#!/usr/bin/env python3
# coding: UTF-8
# Setting Controller
import time
import threading
import glob
import os.path
from mode import Mode 
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class SettingController(threading.Thread):
    u""" 設定ファイルを定期的に確認してLED制御するクラス
    """
    def __init__(self, setting_path):
        threading.Thread.__init__(self)

        logger.debug("SettingController init")
        self.setting_path = setting_path
        self.mode = None
    def run(self):
        u""" 設定ファイル定期読み込み開始
        """
        logger.debug("Setting Controller Execute")
        while True:
            target = os.path.join(self.setting_path,"*")
            for file in glob.glob(target):
                for line in open(file, "r"):
                    logger.debug("Found file:" + file + " value:" + line)
                    if os.path.basename(file) == "mode" :
                        if line.strip() == "date":
                            logger.debug("Found date")
                            self.mode = Mode.DATE
                        elif line.strip() == "clock":
                            logger.debug("Found clock")
                            self.mode = Mode.CLOCK
                        elif line.strip() == "temp":
                            logger.debug("Found temp")
                            self.mode = Mode.TEMP
                        elif line.strip() == "meigen":
                            logger.debug("Found meigen")
                            self.mode = Mode.MEIGEN
                        # 読み込み後ファイルを消す
                        os.remove(os.path.join(self.setting_path,"mode"))
            time.sleep(2)
    def get(self):
        u"""値を取得されたらNoneにする
        """
        mode = self.mode
        self.mode = None
        return mode


# Main function
if __name__ == "__main__":
    setting_thread = threading.Thread(target=setting_obj.execute, name="setting")
    setting_thread.setDaemon(True)
    setting_thread.start()
    while True:
        time.sleep(0.01)

