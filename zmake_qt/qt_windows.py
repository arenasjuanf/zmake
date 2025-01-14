import subprocess
import webbrowser

from PySide2.QtWidgets import QMainWindow

import zmake
from zmake.utils import APP_PATH
from zmake_qt._guide_window import Ui_GuideWindow
from zmake_qt._progress_window import Ui_ProgressWindow


# noinspection PyMethodMayBeStatic
class GuideWindow(QMainWindow, Ui_GuideWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.guide_label.setText(zmake.GUIDE)
        self.btn_backup.clicked.connect(self.open_backup_dir)
        self.btn_config.clicked.connect(self.open_config_dir)
        self.btn_donate.clicked.connect(self.go_donate)
        self.btn_website.clicked.connect(self.go_website)

    def open_backup_dir(self):
        if not (APP_PATH / "backup").is_dir():
            (APP_PATH / "backup").mkdir()
        subprocess.run(["open", APP_PATH / "backup"])

    def open_config_dir(self):
        subprocess.run(["open", APP_PATH / "data"])

    def go_donate(self):
        webbrowser.open("https://melianmiko.ru/donate")

    def go_website(self):
        webbrowser.open("https://melianmiko.ru/en/zmake")


class ProgressWindow(QMainWindow, Ui_ProgressWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def remove_progress(self):
        self.progressBar.hide()

    def write_log(self, msg):
        self.log_view.append(msg)
