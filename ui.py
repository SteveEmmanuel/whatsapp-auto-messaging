import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QFileDialog, QLabel, QPlainTextEdit
from PyQt5.QtCore import pyqtSlot

primary_font = QtGui.QFont("Roboto", 12, QtGui.QFont.Medium)
primary_sub_font = QtGui.QFont("Roboto", 10, QtGui.QFont.Light)
sub_text_pre_font = QtGui.QFont("Roboto", 8, QtGui.QFont.Medium)
sub_text_font = QtGui.QFont("Roboto", 8, QtGui.QFont.Light)


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.selected_image_label = QLabel()
        self.select_image_sub_label = QLabel()
        self.select_image = QPushButton()
        self.select_image_label = QLabel()
        self.selected_input_file_label = QLabel()
        self.select_input_file = QPushButton()
        self.select_input_file_label = QLabel()
        self.horizontal_group_box = QGroupBox()
        self.selected_input_file_label_pre = QLabel()
        self.message_box_label = QLabel()
        self.message_box_sub_label = QLabel()
        self.selected_image_label_pre = QLabel()
        self.message_box = QPlainTextEdit()
        self.send_button = QPushButton()
        self.title = 'Whatsapp Auto-Messaging'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.input_file_path = ''
        self.image_file_path = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        window_layout = QVBoxLayout()
        window_layout.addWidget(self.horizontal_group_box)
        self.setLayout(window_layout)

        self.show()

    def createGridLayout(self):
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        self.select_input_file_label.setText("Select Input csv file")
        self.select_input_file_label.setFont(primary_font)
        layout.addWidget(self.select_input_file_label, 0, 0)

        self.select_input_file.setText("Browse Files")
        layout.addWidget(self.select_input_file, 0, 1)

        self.selected_input_file_label_pre.setText("Input file Selected: ")
        self.selected_input_file_label_pre.setFont(sub_text_pre_font)
        layout.addWidget(self.selected_input_file_label_pre, 2, 0)

        self.selected_input_file_label.setText("")
        self.selected_input_file_label.setFont(sub_text_font)
        layout.addWidget(self.selected_input_file_label, 2, 1)

        self.select_image_label.setText("Select the Image you want to send.")
        self.select_image_label.setFont(primary_font)
        layout.addWidget(self.select_image_label, 3, 0)

        self.select_image_sub_label.setText("(Leave it empty if not required.)")
        self.select_image_sub_label.setFont(primary_sub_font)
        layout.addWidget(self.select_image_sub_label, 4, 0)

        self.select_image.setText("Browse Files")
        layout.addWidget(self.select_image, 3, 1)

        self.selected_image_label_pre.setText("Image File Selected: ")
        self.selected_image_label_pre.setFont(sub_text_pre_font)
        layout.addWidget(self.selected_image_label_pre, 6, 0)

        self.selected_image_label.setText("")
        self.selected_image_label.setFont(sub_text_font)
        layout.addWidget(self.selected_image_label, 6, 1)

        self.message_box_label.setText("Enter the message to be sent:")
        self.message_box_label.setFont(primary_font)
        layout.addWidget(self.message_box_label, 7, 0)

        self.message_box_sub_label.setText(
            "(Enter the characters {} wherever you want to substitute the Customer name in the message.)")
        self.message_box_sub_label.setFont(primary_sub_font)
        layout.addWidget(self.message_box_sub_label, 8, 0)

        layout.addWidget(self.message_box, 9, 0)

        self.send_button.setText("Send")
        layout.addWidget(self.send_button, 10, 1)

        self.select_input_file.clicked.connect(self.open_file_name_dialog)
        self.select_image.clicked.connect(self.open_file_name_dialog)

        self.horizontal_group_box.setLayout(layout)

    @pyqtSlot()
    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileNames()", "",
                                              "All Files (*);;Python Files (*.py)", options=options)
        if file:
            print(file)
            if self.sender() is self.select_input_file:
                print('Selected input file: ' + file)
                self.selected_input_file_label.setText(file)
                self.input_file_path = file
            elif self.sender() is self.select_image:
                print('Selected image file: ' + file)
                self.selected_image_label.setText(file)
                self.image_file_path = file


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
