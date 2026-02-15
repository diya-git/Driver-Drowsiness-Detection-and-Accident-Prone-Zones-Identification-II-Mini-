import threading
import winsound
import time


class Alarm:
    def __init__(self):
        self.alarm_on = False

    def beep_loop(self):
        while self.alarm_on:
            winsound.Beep(1000, 500)  # 1000 Hz, 500 ms
            time.sleep(0.1)

    def start(self):
        if not self.alarm_on:
            self.alarm_on = True
            threading.Thread(target=self.beep_loop, daemon=True).start()

    def stop(self):
        self.alarm_on = False
