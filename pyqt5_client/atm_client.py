# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

KEYS_STYLESHEET = 'background-color: rgb(206, 206, 206);'

BTN_STYLESHEET = "QPushButton\n{\n  background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n                                    stop: 0 rgb(120,120,120), stop: 1 rgb(80,80,80));\n  border: 1px solid rgb(20,20,20);\n  color: rgb(230,230,230);\n  padding: 4px 8px;\n}\nQPushButton:hover\n{\n  background-color: rgb(70,110,130);\n}\nQPushButton:pressed\n{\n  border-color: rgb(90,200,255);\n  padding: 1px -1px -1px 1px;\n}\nQPushButton:checked\n{\n  background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n                                    stop: 0 rgb(40,150,200), stop: 1 rgb(90,200,255));\n  color: rgb(20,20,20);\n}\n\nQPushButton:checked:hover\n{\n  background-color: rgb(70,110,130);\n}\nQPushButton:disabled\n{\n  background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n                                    stop: 0 rgb(160,160,160), stop: 1 rgb(120,120,120));\n  border-color: rgb(60,60,60);\n  color: rgb(40,40,40);\n}"

class NumButton(QtWidgets.QPushButton):

    '''
    Custom class for num keys
    We created this class to add num_signal
    '''

    num_signal = QtCore.pyqtSignal(QtWidgets.QPushButton)
    def __init__(self, parent=None):
        super(NumButton, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit(True)
        self.num_signal.emit(self)
        
class CustomQLabel(QtWidgets.QLabel):

    '''
    Custom QLabel class with mouse press event
    '''

    clicked=QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(958, 669)

        self.action = None  # we want to know what action the user is going to perform
        self.curr_screen = 0    # initial screen is 0

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.screen_panel = QtWidgets.QFrame(self.centralwidget)
        self.screen_panel.setGeometry(QtCore.QRect(250, 10, 400, 300))
        self.screen_panel.setAutoFillBackground(False)
        self.screen_panel.setStyleSheet("background-color: rgb(0, 145, 0);")
        self.screen_panel.setFrameShape(QtWidgets.QFrame.Panel)
        self.screen_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.screen_panel.setObjectName("screen_panel")
        self.gridLayoutWidget = QtWidgets.QWidget(self.screen_panel)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.change_pin_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.change_pin_btn.setObjectName("change_pin_btn")
        self.change_pin_btn.setStyleSheet(BTN_STYLESHEET)
        self.gridLayout.addWidget(self.change_pin_btn, 1, 2, 1, 1)
        self.withdraw_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.withdraw_btn.setObjectName("withdraw_btn")
        self.withdraw_btn.setStyleSheet(BTN_STYLESHEET)
        self.gridLayout.addWidget(self.withdraw_btn, 0, 0, 1, 1)
        self.deposit_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.deposit_btn.setObjectName("deposit_btn")
        self.deposit_btn.setStyleSheet(BTN_STYLESHEET)
        self.gridLayout.addWidget(self.deposit_btn, 1, 0, 1, 1)
        self.balance_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.balance_btn.setObjectName("balance_btn")
        self.balance_btn.setStyleSheet(BTN_STYLESHEET)
        self.change_pin_btn.clicked.connect(self.create_pin_entry_screen)
        self.deposit_btn.clicked.connect(self.create_pin_entry_screen)
        self.balance_btn.clicked.connect(self.create_pin_entry_screen)
        self.withdraw_btn.clicked.connect(self.create_pin_entry_screen)
        self.gridLayout.addWidget(self.balance_btn, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(100, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.movie = QtGui.QMovie('C:/Users/Dimitris/Desktop/atm.gif')
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie_lbl = CustomQLabel(self.centralwidget)
        self.movie_lbl.setGeometry(self.screen_panel.geometry())
        self.movie_lbl.setMinimumSize(self.screen_panel.size())
        self.movie_lbl.setMovie(self.movie)
        self.movie_lbl.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.movie_lbl.clicked.connect(self.on_click_gif)
        self.movie.start()
        self.keys_panel = QtWidgets.QFrame(self.centralwidget)
        self.keys_panel.setGeometry(QtCore.QRect(270, 330, 361, 291))
        self.keys_panel.setStyleSheet("background-color: rgb(154, 154, 154);")
        self.keys_panel.setFrameShape(QtWidgets.QFrame.Panel)
        self.keys_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.keys_panel.setObjectName("keys_panel")
        self.num1_btn = NumButton(self.keys_panel)
        self.num1_btn.setGeometry(QtCore.QRect(10, 10, 61, 61))
        self.num1_btn.setFont(font)
        self.num1_btn.setAutoFillBackground(False)
        self.num1_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num1_btn.setObjectName("num1_btn")
        self.num4_btn = NumButton(self.keys_panel)
        self.num4_btn.setGeometry(QtCore.QRect(10, 80, 61, 61))
        self.num4_btn.setFont(font)
        self.num4_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num4_btn.setObjectName("num4_btn")
        self.num7_btn = NumButton(self.keys_panel)
        self.num7_btn.setGeometry(QtCore.QRect(10, 150, 61, 61))
        self.num7_btn.setFont(font)
        self.num7_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num7_btn.setObjectName("num7_btn")
        self.num2_btn = NumButton(self.keys_panel)
        self.num2_btn.setGeometry(QtCore.QRect(100, 10, 61, 61))
        self.num2_btn.setFont(font)
        self.num2_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num2_btn.setObjectName("num2_btn")
        self.num8_btn = NumButton(self.keys_panel)
        self.num8_btn.setGeometry(QtCore.QRect(100, 150, 61, 61))
        self.num8_btn.setFont(font)
        self.num8_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num8_btn.setObjectName("num8_btn")
        self.num5_btn = NumButton(self.keys_panel)
        self.num5_btn.setGeometry(QtCore.QRect(100, 80, 61, 61))
        self.num5_btn.setFont(font)
        self.num5_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num5_btn.setObjectName("num5_btn")
        self.num3_btn = NumButton(self.keys_panel)
        self.num3_btn.setGeometry(QtCore.QRect(190, 10, 61, 61))
        self.num3_btn.setFont(font)
        self.num3_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num3_btn.setObjectName("num3_btn")
        self.num9_btn = NumButton(self.keys_panel)
        self.num9_btn.setGeometry(QtCore.QRect(190, 150, 61, 61))
        self.num9_btn.setFont(font)
        self.num9_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num9_btn.setObjectName("num9_btn")
        self.num6_btn = NumButton(self.keys_panel)
        self.num6_btn.setGeometry(QtCore.QRect(190, 80, 61, 61))
        self.num6_btn.setFont(font)
        self.num6_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num6_btn.setObjectName("num6_btn")
        self.num0_btn = NumButton(self.keys_panel)
        self.num0_btn.setGeometry(QtCore.QRect(100, 220, 61, 61))
        self.num0_btn.setFont(font)
        self.num0_btn.setStyleSheet(KEYS_STYLESHEET)
        self.num0_btn.setObjectName("num0_btn")

        self.set_num_key_slots()

        self.clear_btn = QtWidgets.QPushButton(self.keys_panel)
        self.clear_btn.setGeometry(QtCore.QRect(280, 10, 61, 61))
        self.clear_btn.setStyleSheet("background-color: rgb(207, 207, 0);")
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(self.clear_operation)
        self.ok_btn = QtWidgets.QPushButton(self.keys_panel)
        self.ok_btn.setGeometry(QtCore.QRect(280, 150, 61, 61))
        self.ok_btn.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.ok_btn.setObjectName("ok_btn")
        self.cancel_btn = QtWidgets.QPushButton(self.keys_panel)
        self.cancel_btn.setGeometry(QtCore.QRect(280, 80, 61, 61))
        self.cancel_btn.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.cancel_operation)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 958, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_num_key_slots(self):
        '''
        We set the slots in order to know
        what to type when a specific num key is pressed
        '''
        self.num0_btn.num_signal.connect(self.type_num)
        self.num1_btn.num_signal.connect(self.type_num)
        self.num2_btn.num_signal.connect(self.type_num)
        self.num3_btn.num_signal.connect(self.type_num)
        self.num4_btn.num_signal.connect(self.type_num)
        self.num5_btn.num_signal.connect(self.type_num)
        self.num6_btn.num_signal.connect(self.type_num)
        self.num7_btn.num_signal.connect(self.type_num)
        self.num8_btn.num_signal.connect(self.type_num)
        self.num9_btn.num_signal.connect(self.type_num)

    def on_click_gif(self):
        '''
        When the animation is clicked, show main menu
        '''
        self.movie_lbl.setParent(None)
        self.curr_screen = 1    # menu screen is 1

    def create_pin_entry_screen(self):
        '''
        When user chooses to proceed with an operation,
        create & show the pin enter screen (screen 2)
        '''

        self.curr_screen = 2    # pin entry screen is 2

        self.action = self.MainWindow.sender().text().upper()

        self.balance_btn.setParent(None)
        self.withdraw_btn.setParent(None)
        self.deposit_btn.setParent(None)
        self.change_pin_btn.setParent(None)
        self.pin_lineedit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.pin_lineedit.setReadOnly(True)
        self.pin_lineedit.textChanged.connect(self.on_pin_text_changed)
        self.pin_lineedit.setMaximumSize(QtCore.QSize(210, 20))
        self.pin_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pin_lineedit.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.pin_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pin_lineedit.setAlignment(QtCore.Qt.AlignCenter) 
        self.pin_lineedit.setObjectName("pin_lineedit")
        self.gridLayout.addWidget(self.pin_lineedit, 1, 1, 1, 1)
        self.enter_pin_lbl = QtWidgets.QLabel(self.gridLayoutWidget)
        self.enter_pin_lbl.setMaximumSize(QtCore.QSize(210, 30))
        self.enter_pin_lbl.setText("Please enter your pin")
        self.gridLayout.addWidget(self.enter_pin_lbl, 0, 1, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.enter_pin_lbl.setFont(font)
        self.enter_pin_lbl.setStyleSheet("color: rgb(255, 255, 255);")
        self.enter_pin_lbl.setObjectName("enter_pin_lbl")

        if self.action == 'WITHDRAWAL' or self.action == 'DEPOSITION': self.ok_btn.clicked.connect(self.create_amount_entry_screen)
        elif self.action == 'CHANGE PIN': self.ok_btn.clicked.connect(self.create_new_pin_enter_screen)
        # else: self.ok_btn.clicked.connect()

    def create_new_pin_enter_screen(self):
        '''
        If user chooses to change pin,
        create & show the new pin enter screen
        '''

        self.curr_screen = 4    # create new pin screen is 4

        try:
            self.gridLayout.removeWidget(self.pin_lineedit) # deleting previous screen's widgets
            self.gridLayout.removeWidget(self.enter_pin_lbl)

            self.enter_new_pin_lbl = self.enter_pin_lbl
            self.new_pin_lineedit = self.pin_lineedit

            self.enter_new_pin_lbl.setMaximumSize(QtCore.QSize(250, 30))
            self.new_pin_lineedit.setMaximumSize(QtCore.QSize(250, 20))
            self.enter_new_pin_lbl.setText("Please enter your new pin")
            self.new_pin_lineedit.clear()

            self.gridLayout.addWidget(self.enter_new_pin_lbl, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.new_pin_lineedit, 1, 1, 1, 1)
        except Exception as e:
            print(e)

    def create_amount_entry_screen(self):
        '''
        If the action is deposition or withdrawal,
        the enter amount screen is showed to user
        '''
        self.curr_screen = 3    # amount entry screen is 3
        try:
            self.gridLayout.removeWidget(self.pin_lineedit) # deleting previous screen's widgets
            self.gridLayout.removeWidget(self.enter_pin_lbl)

            self.enter_amount_lbl = self.enter_pin_lbl
            self.amount_lineedit = self.pin_lineedit

            self.gridLayout.addWidget(self.enter_amount_lbl, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.amount_lineedit, 1, 1, 1, 1)

            self.enter_amount_lbl.setMaximumSize(QtCore.QSize(240, 30))
            self.enter_amount_lbl.setText("Please enter an amount")
            self.amount_lineedit.disconnect()
            self.amount_lineedit.setMaximumSize(QtCore.QSize(220, 20))
            self.amount_lineedit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.amount_lineedit.clear()

        except Exception as e:
            print(e)

    def on_pin_text_changed(self):
        '''
        We ensure that the user wont enter a pin whose
        length is more that 4 digits
        '''
        try:
            if len(self.pin_lineedit.text()) > 4:
                self.pin_lineedit.setText(self.pin_lineedit.text()[:-1])
        except Exception as e:
            print(e)

    def okay_pressed(self):
        '''
        After ok pressed
        '''
        self.pin = self.pin_lineedit.text()

    def type_num(self, key):
        '''
        When a key is pressed, fill qlineEdit with appropriate num
        '''
        try:
            tmp_str = self.pin_lineedit.text()
            tmp_str += ''.join(i for i in key.text() if i.isdigit())
            self.pin_lineedit.setText(tmp_str)
        except Exception as e:
            print(e)

    def clear_operation(self):
        '''
        When clear btn is clicked, clear the qlineEdit
        '''
        try:
            if self.curr_screen == 2:
                self.pin_lineedit.clear()
            elif self.curr_screen == 3:
                self.amount_lineedit.clear()
            elif self.curr_screen == 4:
                self.new_pin_lineedit.clear()
        except Exception as e:
            print(e)
    
    def cancel_operation(self):
        '''
        If cancel btn is clicked, initialize again the ui
        '''
        try:
            self.setupUi(self.MainWindow)
        except Exception as e:
            print(e)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "ATM Client"))
        self.num1_btn.setText(_translate("MainWindow", "1"))
        self.num4_btn.setText(_translate("MainWindow", "4"))
        self.num7_btn.setText(_translate("MainWindow", "7"))
        self.num2_btn.setText(_translate("MainWindow", "2"))
        self.num8_btn.setText(_translate("MainWindow", "8"))
        self.num5_btn.setText(_translate("MainWindow", "5\n""-"))
        self.num3_btn.setText(_translate("MainWindow", "3"))
        self.num9_btn.setText(_translate("MainWindow", "9"))
        self.num6_btn.setText(_translate("MainWindow", "6"))
        self.balance_btn.setText(_translate("MainWindow", "Balance Enquiry"))
        self.withdraw_btn.setText(_translate("MainWindow", "Withdrawal"))
        self.deposit_btn.setText(_translate("MainWindow", "Deposition"))
        self.change_pin_btn.setText(_translate("MainWindow", "Change Pin"))
        self.clear_btn.setText(_translate("MainWindow", "CLEAR"))
        self.ok_btn.setText(_translate("MainWindow", "OK"))
        self.cancel_btn.setText(_translate("MainWindow", "CANCEL"))
        self.num0_btn.setText(_translate("MainWindow", "0"))

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
