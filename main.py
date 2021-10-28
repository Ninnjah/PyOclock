import sys
import time

from PyQt5 import QtWidgets
from PyQt5.Qt import QTimer
from PyQt5.QtCore import QTime

from ui.main_ui import Ui_MainWindow as MainWindow


class ClockUI(QtWidgets.QMainWindow, MainWindow):
    clock_timer: QTimer
    stopwatch_timer: QTimer
    stopwatch_time: float
    stopwatch_laps: int = 0
    timer_timer: QTimer
    timer_time: int = 0
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

        # Set timer timer
        self.timer_timer = QTimer(self)
        self.timer_timer.setInterval(1000)
        self.timer_timer.timeout.connect(self.update_timer)

        # Set buttons
        self.button_stopwatch.clicked.connect(self.start_stopwatch)
        self.button_stopwatch_rec.clicked.connect(self.add_rec_stopwatch)
        self.button_stopwatch_rec.setEnabled(False)
        self.button_stat_reset.clicked.connect(self.reset_rec_stopwatch)
        self.button_timer.clicked.connect(self.start_timer)
        # timer time button set
        self.add_10min.clicked.connect(lambda: self.timer_time_set(600))
        self.add_min.clicked.connect(lambda: self.timer_time_set(60))
        self.add_10sec.clicked.connect(lambda: self.timer_time_set(10))
        self.add_sec.clicked.connect(lambda: self.timer_time_set(1))
        self.dec_10min.clicked.connect(lambda: self.timer_time_set(-600))
        self.dec_min.clicked.connect(lambda: self.timer_time_set(-60))
        self.dec_10sec.clicked.connect(lambda: self.timer_time_set(-10))
        self.dec_sec.clicked.connect(lambda: self.timer_time_set(-1))

    def start_stopwatch(self) -> None:
        """Toggle stopwatch timer"""
        if self.button_stopwatch.text() == "Старт":
            self.button_stopwatch.setText("Стоп")
            self.stopwatch_time = time.monotonic()
            self.stopwatch_timer.start()
            self.button_stopwatch_rec.setEnabled(True)

        else:
            self.button_stopwatch.setText("Старт")
            self.stopwatch_timer.stop()
            self.button_stopwatch_rec.setEnabled(False)

    def start_timer(self) -> None:
        """Toggle timer timer"""
        if self.button_timer.text() == "Старт":
            self.button_timer.setText("Стоп")
            self.timer_timer.start()

        else:
            self.button_timer.setText("Старт")
            self.timer_timer.stop()

    def update_clock(self) -> None:
        """Updates clock LCD"""
        current_time: QTime = QTime.currentTime()
        str_current_time: str = current_time.toString("hh:mm")
        self.LCD.display(str_current_time)

    def update_stopwatch(self) -> None:
        """Updates stopwatch LCD"""
        current_time: float = time.monotonic()

        str_current_time: str = time.strftime(
            "%M:%S:", time.gmtime(current_time - self.stopwatch_time)
        )

        self.LCD_stopwatch.display(
            f"{str_current_time}{int(current_time*100)%100:02d}"
        )

    def update_timer(self) -> None:
        """Updates timer LCD and decrease timer time every second"""
        self.timer_time -= 1

        if self.timer_time <= 0:
            str_current_time: str = "S70P"

        else:
            str_current_time: str = time.strftime(
                "%M:%S:", time.gmtime(self.timer_time)
            )

        self.LCD_timer.display(str_current_time)

    def add_rec_stopwatch(self) -> None:
        """Writes lap time to TextEdit under stopwatch"""
        self.stopwatch_laps += 1
        current_time: float = time.monotonic()

        str_current_time: str = time.strftime(
            "%M:%S:", time.gmtime(current_time - self.stopwatch_time)
        )

        self.stopwatch_stat.append(
            f"Круг {self.stopwatch_laps}: {str_current_time}{int(current_time*100)%100:02d}"
        )

    def reset_rec_stopwatch(self) -> None:
        """Deletes every lap time from TextEdit under stopwatch"""
        self.stopwatch_stat.setText("")
        self.stopwatch_laps = 0

    def timer_time_set(self, secs: int) -> None:
        """Set timer time"""
        self.timer_time += secs

        if self.timer_time < 0:
            self.timer_time = 0

        elif self.timer_time > 3599:
            self.timer_time = 3599

        str_current_time: str = time.strftime(
            "%M:%S:", time.gmtime(self.timer_time)
        )
        self.LCD_timer.display(str_current_time)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = ClockUI()
    window.show()

    sys.exit(app.exec_())
