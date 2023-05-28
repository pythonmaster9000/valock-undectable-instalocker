import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QApplication, QMainWindow, QLabel, \
    QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QBitmap, QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QEvent, QObject
from PyQt5 import QtTest
import json
import asyncio
from PIL import Image
import pystray
from pystray import MenuItem as item
import time

pathim = r"assets\mainscreen.png"
scuffed_timer = [False, time.time()]


class FocusHandler(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            if self.parent.isVisible():
                scuffed_timer[0] = True
                scuffed_timer[1] = time.time()
                self.parent.hide()
        elif event.type() == QEvent.FocusOut:
            if obj == self.parent:
                self.parent.hide()
        return super().eventFilter(obj, event)


class MainWindow(QMainWindow):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.Tool)
        pixmap = QPixmap(pathim)
        mask = pixmap.createMaskFromColor(Qt.transparent)
        self.setMask(mask)
        label = QLabel(self)
        label.setPixmap(pixmap)
        self.chosen_button = None
        self.setCentralWidget(label)
        self.makebuttons()

    def hideandquit(self):
        self.hide()
        self.quit()

    def makebuttons(self):
        with open(r'config.json') as file:
            agents = json.load(file)['agents']
        x = 32
        y = 100
        for agent in agents:
            button = QPushButton(self)
            # button.clicked.connect(lambda: a function that changes the json DB for my preference)
            button.setCheckable(True)
            button.setProperty("agent", agent)
            button.clicked.connect(lambda checked, btn=button: self.selectbutton(checked, btn))
            button_icon = QPixmap(rf'assets\{agent}_icon.png')
            button.setIcon(QIcon(button_icon))
            button.setIconSize(button_icon.size())
            button.setGeometry(x, y, button_icon.width(), button_icon.height())
            button.setStyleSheet("background-color: transparent; border: none;")
            x += 70
            if x > 280:
                x = 32
                y += 50

    def selectbutton(self, checked, button):
        with open(r'config.json') as file:
            agents = json.load(file)
        if checked:
            if self.chosen_button is not None:
                self.chosen_button.setChecked(False)
                # button_icon = QPixmap(
                #    rf'C:\Users\riode\OneDrive\Desktop\valockproject\assets\{self.chosen_button.property("agent")}_icon.png')
                # self.chosen_button.setIcon(QIcon(button_icon))
                self.chosen_button.setStyleSheet("background-color: transparent; border: none;")
            self.chosen_button = button
            self.agent[0] = agents['agents'][self.chosen_button.property("agent")]
            agents['preferrence']['pref'] = agents['agents'][self.chosen_button.property("agent")]
            with open(r'config.json', 'w') as outfile:
                json.dump(agents, outfile, indent=4)
            # button_icon = QPixmap(rf'C:\Users\riode\OneDrive\Desktop\valockproject\assets\reyna_icon.png')
            # self.chosen_button.setIcon(QIcon(button_icon))
            self.chosen_button.setStyleSheet("background: red")
            # self.chosen_button.setStyleSheet("border: blue")
        # else:
        #    # deselect button
        #    #button_icon = QPixmap(
        #    #    rf'C:\Users\riode\OneDrive\Desktop\valockproject\assets\{self.chosen_button.property("agent")}_icon.png')
        #    #self.chosen_button.setIcon(QIcon(button_icon))
        #    self.chosen_button.setStyleSheet("background-color: transparent; border: none;")
        #    self.chosen_button = None


def rungui(agent):
    app = QApplication(sys.argv)
    main_window = MainWindow(agent)
    main_window.move(1335, 625)
    focus_handler = FocusHandler(main_window)
    main_window.installEventFilter(focus_handler)

    def toggle_window():
        if main_window.isVisible():
            main_window.hide()
        else:
            if scuffed_timer[0]:
                scuffed_timer[0] = False
                if time.time() - scuffed_timer[1] < 0.3:
                    return
            spawn_location = QCursor.pos()
            main_window.move(spawn_location.x() - 420, spawn_location.y() - 430)
            main_window.show()
            main_window.activateWindow()
            main_window.raise_()

    def exitapp():
        exit()

    tray_icon = QSystemTrayIcon(QIcon(rf'assets\valicon.ico'), app)
    tray_menu = QMenu()
    exit_action = QAction("Exit", app)
    exit_action.triggered.connect(exitapp)
    tray_menu.addAction(exit_action)
    toggle_action = QAction("Open/Close", app)
    toggle_action.triggered.connect(toggle_window)
    # tray_menu.addAction(toggle_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(toggle_window)
    tray_icon.show()
    sys.exit(app.exec_())
