import sys
from typing import Tuple

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTimer, QProgressBar

from ui.main_ui import Ui_MainWindow as MainWindow


class ClockUI(QtWidgets.QMainWindow, MainWindow):
    clock_timer: QTimer
    stopwatch_timer: QTimer
    timer_timer: QTimer
    timer_time: int
    timer_progress_list: tuple

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.timer_progress_list = (
            self.timer_progress,
            self.timer_progress_2,
            self.timer_progress_3,
            self.timer_progress_4,
            self.timer_progress_5,
            self.timer_progress_6,
        )
        for i in self.timer_progress_list:
            i.setValue(0)

        self.LCD.display("00:00")
        self.LCD_stopwatch.display("00:00:00")
        self.LCD_timer.display("00:00")

        # Set clock timer
        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start()

    def update_clock(self):
        current_time = QtCore.QTime.currentTime()
        str_current_time = current_time.toString('hh:mm')
        self.LCD.display(str_current_time)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = ClockUI()
    window.show()

    sys.exit(app.exec_())
