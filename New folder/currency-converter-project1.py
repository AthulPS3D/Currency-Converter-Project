from typing import List
from PyQt5.QtGui import QFont, QIcon, QPixmap
import requests
import json
import sys
import PyQt5.QtWidgets as qtw
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QWidget,
)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Converter")
        self.setWindowIcon(QIcon("convert.png"))
        self.setMinimumSize(300, 150)

        URL = 'https://api.exchangerate-api.com/v4/latest/USD'

        r = requests.get(URL).json()

        data = r['rates']

        listitem = list(r['rates'].keys())

        # Create a QGridLayout instance
        layout = QGridLayout()

        heading = qtw.QLabel("Currency Converter")
        heading.setFont(QFont('Helvetica', 15))

        # label
        from_label = qtw.QLabel("From: ")
        to_label = qtw.QLabel("To: ")

        # QLineEdit
        from_currency = qtw.QLineEdit()
        to_currency = qtw.QLineEdit("0.00")

        # dropdown
        from_opt = qtw.QComboBox(self)
        for item in listitem:
            from_opt.addItem(item)
        from_opt.setCurrentText('USD')

        to_opt = qtw.QComboBox(self)
        for item in listitem:
            to_opt.addItem(item)
        to_opt.setCurrentText('INR')

        # button
        cb = qtw.QPushButton("", clicked=lambda: interchange())
        cb.setIcon(QIcon("refresh.png"))

        convert_button = qtw.QPushButton("Convert", clicked=lambda: convert())

        # Add widgets to the layout
        layout.addWidget(heading, 0, 1)

        layout.addWidget(from_label, 1, 0)
        layout.addWidget(from_currency, 1, 1)
        layout.addWidget(from_opt, 1, 2)

        layout.addWidget(cb, 3, 2)

        layout.addWidget(to_label, 4, 0)
        layout.addWidget(to_currency, 4, 1)
        layout.addWidget(to_opt, 4, 2)

        layout.addWidget(convert_button, 5, 1)

        # Set the layout on the application's window
        self.setLayout(layout)

        # Function to convert currency
        def convert():
            amount = float(from_currency.text())
            from_cur = from_opt.currentText()
            to_cur = to_opt.currentText()

            if from_cur != "USD":
                amount = amount/data[from_cur]

            amount = round(amount*data[to_cur], 4)

            to_currency.setText(str(amount))

        # Function to interchange
        def interchange():
            temp = from_cur = from_opt.currentText()
            from_opt.setCurrentText(to_opt.currentText())
            to_opt.setCurrentText(temp)


# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())