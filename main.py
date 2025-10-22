import sys
import os
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QSizePolicy)
from PySide6.QtGui import QMovie, QIcon
from layout.build_ui import build_ui
from layout.menu_bar_and_about import setup_menu_bar

# -------------------------|Handling images opened with program as default|------------------------- #
if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    image_path = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GIF Player")
        self.setStyleSheet("background-color: #31363F;")
        self.gif_loaded = False
        self.current_folder = ""
        self.current_image_path = ""
        self.gif_paths_list = ""
        # -------------------------|Icon path handling for packaging|------------------------- #
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "icons", "gif-icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        # -------------------------|building the ui|------------------------- #
        widgets = build_ui()
        self.layout = widgets["layout"]
        self.inner_buttons = widgets["inner_buttons"]
        self.speed_slider = widgets["speed_slider"]
        self.button_pause = widgets["button_pause"]
        self.button_reset = widgets["button_reset"]
        self.button_next = widgets["button_next"]
        self.button_prev = widgets["button_prev"]
        self.gif_layout = widgets["gif_layout"]
        self.main_display = widgets["main_display"]
        menu_bar = setup_menu_bar(self, self.load_gif)
        self.setMenuBar(menu_bar)

        # -------------------------|connecting buttons to methods|------------------------- #
        self.speed_slider.valueChanged.connect(self.speed_control)
        self.button_pause.clicked.connect(self.pause_clicked)
        self.button_reset.clicked.connect(self.reset_speed)
        self.button_next.clicked.connect(self.next_clicked)
        self.button_prev.clicked.connect(self.prev_clicked)

        # -------------------------|logic for playing gif or otherwise showing open option|------------------------- #
        if image_path.lower().endswith(".gif") and os.path.exists(image_path):
            self.current_folder = os.path.dirname(image_path)
            self.current_image_path = image_path
            self.gen_gif_file_list()
            self.gif_image = QMovie(image_path)
            self.gif_image.jumpToFrame(0)
            self.gif_dimensions = self.gif_image.frameRect().size()
            self.main_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.main_display.setScaledContents(False)
            self.main_display.setFixedSize(self.gif_dimensions)
            self.main_display.setMovie(self.gif_image)
            self.gif_image.start()
            self.gif_loaded = True
        # -------------------------|file open option if no gif loaded|------------------------- #
        else:
            self.speed_slider.setDisabled(True)
            self.button_pause.setDisabled(True)
            self.button_reset.setDisabled(True)
            self.button_next.setDisabled(True)
            self.button_prev.setDisabled(True)

            self.main_display.setText("No gif loaded")

            self.load_button = QPushButton("📂 Open GIF")
            self.load_button.setStyleSheet("""
                                            QPushButton {
                                                color: white;
                                                background-color: #3d99f5;
                                                font-size: 15px;
                                            }
                                            QPushButton:hover {
                                                background-color: #2b7cd3;
                                            }
                                        """)
            self.load_button.clicked.connect(self.load_gif)

            self.gif_layout.addWidget(self.main_display)
            self.gif_layout.addSpacing(10)
            self.gif_layout.addWidget(self.load_button)
            self.gif_layout.addStretch()

        # ------------------------|main container bringing everything together|------------------------ #
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setMinimumSize(self.container.sizeHint())
        self.setMinimumWidth(520)
        self.setMinimumSize(self.size())
        self.setCentralWidget(self.container)

    def speed_control(self, value):
        if self.gif_image and self.gif_image.isValid():
            self.gif_image.setSpeed(value)

    def reset_speed(self):
        self.gif_image.setSpeed(100)
        self.speed_slider.setValue(100)

    def pause_clicked(self):
        if self.button_pause.text() == "Pause":
            self.gif_image.setPaused(True)
            self.button_pause.setText("Unpause")
        else:
            self.gif_image.setPaused(False)
            self.button_pause.setText("Pause")

    def prev_clicked(self):
        self.current_image_path = os.path.normpath(self.current_image_path)
        if len(self.gif_paths_list) > 1:
            try:
                index = self.gif_paths_list.index(self.current_image_path)
                prev_index = (index - 1) % len(self.gif_paths_list)
                self.apply_gif(self.gif_paths_list[prev_index])
            except ValueError:
                pass

    def next_clicked(self):
        self.current_image_path = os.path.normpath(self.current_image_path)
        if len(self.gif_paths_list) > 1:
            try:
                index = self.gif_paths_list.index(self.current_image_path)
                next_index = (index + 1) % len(self.gif_paths_list)
                self.apply_gif(self.gif_paths_list[next_index])
            except ValueError:
                pass

    def gen_gif_file_list(self):
        if not self.current_folder or not os.path.isdir(self.current_folder):
            return
        gif_files = [file for file in os.listdir(self.current_folder) if file.lower().endswith(".gif")]
        self.gif_paths_list = [os.path.normpath(os.path.join(self.current_folder, file_name)) for file_name in gif_files]

    # -------------------------|method to maintain gif scale when window resizes|------------------------- #
    def update_gif_scale(self):
        if not self.gif_loaded:
            return
        available_width = self.centralWidget().width()
        available_height = self.centralWidget().height() - self.inner_buttons.height()

        gif_width = self.gif_dimensions.width()
        gif_height = self.gif_dimensions.height()
        gif_ratio = gif_width / gif_height

        if available_width / available_height > gif_ratio:
            scaled_height = available_height
            scaled_width = int(scaled_height * gif_ratio)
        else:
            scaled_width = available_width
            scaled_height = int(scaled_width / gif_ratio)

        scaled_size = QSize(scaled_width, scaled_height)
        self.gif_image.setScaledSize(scaled_size)
        self.main_display.setFixedSize(scaled_size)

    # -------------------------|overwriting methods to change gif size|------------------------- #
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_gif_scale()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_gif_scale()

    # -------------------------|method to load gif and apply to main display|------------------------- #
    def load_gif(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open GIF", "", "GIF Files (*.gif)")
        file_path = os.path.normpath(file_path)
        if file_path:
            self.apply_gif(file_path)
            self.current_folder = os.path.dirname(file_path)
            self.current_image_path = file_path
            self.setWindowTitle(f"GIF Player - {os.path.basename(self.current_image_path)}")
            self.gen_gif_file_list()

    # ----------------|method to apply a gif to the main display|--------------- #
    def apply_gif(self, file_path):
        self.current_image_path = os.path.normpath(file_path)
        if not file_path.lower().endswith(".gif") or not os.path.exists(file_path):
            self.main_display.setText("Invalid GIF file or no GIF selected")
            return

        if self.main_display.movie():
            self.main_display.movie().stop()
            self.main_display.clear()

        self.gif_image = QMovie(file_path)
        if self.gif_image.isValid():
            self.gif_image.jumpToFrame(0)
            self.gif_dimensions = self.gif_image.frameRect().size()
            self.main_display.setMovie(self.gif_image)
            self.gif_image.start()
            self.main_display.adjustSize()
            self.main_display.updateGeometry()
            self.layout.activate()
            self.update_gif_scale()
            self.resize(self.size())
            self.gif_loaded = True
            self.setWindowTitle(f"GIF Player - {os.path.basename(self.current_image_path)}")

            if hasattr(self, "load_button"):
                self.load_button.hide()

            self.speed_slider.setDisabled(False)
            self.button_pause.setDisabled(False)
            self.button_reset.setDisabled(False)
            self.button_next.setDisabled(False)
            self.button_prev.setDisabled(False)
            self.button_pause.setText("Pause")
            self.apply_gif_speed()
        else:
            self.main_display.setText("Invalid GIF file or no GIF selected")

    # ----------------|method used to reset the speed when opening new files, used with small delay|--------------- #
    def apply_gif_speed(self):
        self.gif_image.setSpeed(100)
        # force slider update only if needed
        self.speed_slider.blockSignals(True)
        self.speed_slider.setValue(100 if self.speed_slider.value() != 100 else 99)
        self.speed_slider.setValue(100)
        self.speed_slider.blockSignals(False)

        # refresh slider
        self.speed_slider.update()
        self.inner_buttons.update()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
