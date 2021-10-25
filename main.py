import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTimer

from ui.main_ui import Ui_MainWindow as MainWindow


class ClockUI(QtWidgets.QMainWindow, MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Set display timer
        self.display_timer = QTimer(self)
        self.display_timer.setInterval(1000)
        self.display_timer.timeout.connect(self.update_lcd)
        self.display_timer.start()

    def update_lcd(self):
        current_time = QtCore.QTime.currentTime()
        str_current_time = current_time.toString('hh:mm')
        self.LCD.display(str_current_time)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = ClockUI()
    window.show()

    sys.exit(app.exec_())
