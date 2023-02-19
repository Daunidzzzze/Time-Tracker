import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer


class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Tracker")
        self.setWindowIcon(QIcon('clock_icon.png'))
        self.setGeometry(100, 100, 400, 150)

        self.label = QLabel(self)
        self.label.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("font-size: 20px;")
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet("font-size: 20px;")
        self.stop_button.clicked.connect(self.stop_timer)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.timer_running = False
        self.start_time = None
        self.elapsed_time = None

    def start_timer(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.start_time = time.time()
        self.timer_running = True
        self.update_time()

    def stop_timer(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.timer_running = False
        self.elapsed_time = None
        self.label.setText("00:00:00")

    def update_time(self):
        if self.timer_running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time
            hours, remainder = divmod(self.elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            self.label.setText(time_str)
            QTimer.singleShot(1000, self.update_time)

    def closeEvent(self, event):
        if self.timer_running:
            reply = QMessageBox.question(self, 'Time Tracker',
                                           "Are you sure you want to quit? Your time will not be saved.",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = TimeTracker()
    tracker.show()
    sys.exit(app.exec_())