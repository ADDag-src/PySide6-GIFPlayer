from PySide6.QtWidgets import QMenuBar, QMessageBox


# -------------------------|Menu bar setup|------------------------- #
def setup_menu_bar(main_window, load_gif_callback):
    menu_bar = QMenuBar()
    menu_bar.setStyleSheet("""
        QMenuBar {
            background-color: #444950;
            color: white;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 5px 15px;
        }
        QMenuBar::item:selected {
            background-color: #3d99f5;
        }
        QMenu {
            background-color: #444950;
            color: white;
            border: 1px solid #3d99f5;
        }
        QMenu::item {
            padding: 5px 20px;
            background-color: transparent;
        }
        QMenu::item:selected {
            background-color: #3d99f5;
            color: white;
        }
    """)

    file_menu = menu_bar.addMenu("File")
    open_gif = file_menu.addAction("📂 Open GIF")
    open_gif.triggered.connect(load_gif_callback)

    help_menu = menu_bar.addMenu("Help")
    about_popup = help_menu.addAction("ℹ️ About")
    about_popup.triggered.connect(lambda: show_about(main_window))

    return menu_bar


# -------------------------|custom message box for the about dialog|------------------------- #
def show_about(parent):
    msg = QMessageBox(parent)
    msg.setWindowTitle("About GIF Player")
    msg.setText("This is a lightweight GIF player developed by ADDag-sr.\n\n"
                "You can set this program as the default for opening GIFs.\n\n"
                "Right-click a .gif file → Open with → Choose another app.\n"
                "Select this app executable and check “Always use this app“.")

    msg.setStyleSheet("""
        QLabel {
            color: white;
            font-size: 15px;
        }
        QWidget {
            background-color: #444950;
        }
        QPushButton {
            background-color: #3d99f5;
            color: white;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #5aa0f7;
        }
    """)
    msg.exec()
