from PySide6.QtWidgets import (
    QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QLayout
)
from PySide6.QtCore import Qt


def build_ui():
    layout = QVBoxLayout()

    # -------------------------|bottom control layout and widgets|------------------------- #
    inner_buttons = QWidget()

    speed_label = QLabel("Speed:")
    speed_label.setStyleSheet("color: white; font-size: 15px;")

    speed_slider = QSlider(Qt.Horizontal)
    speed_slider.setFixedHeight(30)
    speed_slider.setMinimum(10)
    speed_slider.setMaximum(300)
    speed_slider.setValue(100)

    button_pause = QPushButton("Pause")
    button_pause.setStyleSheet("color: white; background-color: #3d99f5; font-size: 15px;")

    button_reset = QPushButton("Reset Speed")
    button_reset.setStyleSheet("color: white; background-color: #3d99f5; font-size: 15px;")

    # -------------------------|creating inner layout and adding widgets|------------------------- #
    inner_layout = QHBoxLayout(inner_buttons)
    inner_layout.setSpacing(30)
    inner_layout.addWidget(speed_label)
    inner_layout.addWidget(speed_slider)
    inner_layout.addWidget(button_pause)
    inner_layout.addWidget(button_reset)
    inner_layout.setContentsMargins(20, 20, 20, 20)
    inner_layout.setSizeConstraint(QLayout.SetMinimumSize)

    # -------------------------|wrapper layout to center gif|------------------------- #
    gif_wrapper = QWidget()
    gif_layout = QVBoxLayout(gif_wrapper)
    gif_layout.setContentsMargins(0, 0, 0, 0)
    gif_layout.setAlignment(Qt.AlignCenter)

    # -------------------------|label for playing gif|------------------------- #
    main_display = QLabel()
    main_display.setAlignment(Qt.AlignCenter)
    main_display.setStyleSheet("color: white; font-size: 25px;")

    gif_layout.addWidget(main_display)
    gif_layout.addStretch()
    # add elements to main layout
    layout.addWidget(gif_wrapper)
    layout.addWidget(inner_buttons)

    # return widgets
    return {
        "layout": layout,
        "inner_buttons": inner_buttons,
        "speed_slider": speed_slider,
        "button_pause": button_pause,
        "button_reset": button_reset,
        "gif_layout": gif_layout,
        "main_display": main_display
    }
