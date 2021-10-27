import sys
import time
from typing import Tuple

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTimer, QProgressBar

from ui.main_ui import Ui_MainWindow as MainWindow


class ClockUI(QtWidgets.QMainWindow, MainWindow):
    clock_timer: QTimer
    stopwatch_timer: QTimer
    stopwatch_time: float
    stopwatch_laps: int = 0
    timer_timer: QTimer
    timer_time: int
    timer_progress_list: tuple

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Setup UI
        self.timer_progress_list = (
            self.timer_progress,
            self.timer_progress_2,
            self.timer_progress_3,
            self.timer_progress_4,
            self.timer_progress_5,
            self.timer_progress_6,
        )
        for i in self.timer_progress_list:
            i.setValue(20)

        self.LCD.display("00:00")
        self.LCD_stopwatch.display("00:00:00")
        self.LCD_timer.display("00:00")

        # Set clock timer
        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start()

        # Set stopwatch timer
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.setInterval(1)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch)

        # Set buttons
        self.button_stopwatch.clicked.connect(self.start_stopwatch)
        self.button_stopwatch_rec.clicked.connect(self.add_rec_stopwatch)
        self.button_stat_reset.clicked.connect(self.reset_rec_stopwatch)

    def start_stopwatch(self):
        if self.button_stopwatch.text() == "Старт":
            self.button_stopwatch.setText("Стоп")
            self.stopwatch_time = time.monotonic()
            self.stopwatch_timer.start()
        else:
            self.button_stopwatch.setText("Старт")
            self.stopwatch_timer.stop()

    def update_clock(self):
        current_time = QtCore.QTime.currentTime()
        str_current_time = current_time.toString("hh:mm")
        self.LCD.display(str_current_time)

    def update_stopwatch(self):
        current_time: float = time.monotonic()

        str_current_time = time.strftime(
            "%M:%S:", time.gmtime(current_time - self.stopwatch_time)
        )

        self.LCD_stopwatch.display(
            f"{str_current_time}{int(current_time*100)%100:02d}"
        )

    def add_rec_stopwatch(self):
        self.stopwatch_laps += 1
        current_time: float = time.monotonic()

        str_current_time = time.strftime(
            "%M:%S:", time.gmtime(current_time - self.stopwatch_time)
        )

        self.stopwatch_stat.append(
            f"Круг {self.stopwatch_laps}: {str_current_time}{int(current_time*100)%100:02d}"
        )

    def reset_rec_stopwatch(self):
        self.stopwatch_stat.setText("")
        self.stopwatch_laps = 0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = ClockUI()
    window.show()

    sys.exit(app.exec_())
