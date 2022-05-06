import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QFileDialog, QLabel, QPlainTextEdit, QMessageBox
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
        self.input_file_path = None
        self.image_file_path = None
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

        self.send_button.clicked.connect(self.send_message)

        self.horizontal_group_box.setLayout(layout)

    @pyqtSlot()
    def send_message(self):
        if self.input_file_path is None:
            self.showdialog(message='Input csv File not selected!', dialog_type='error')
            return

        message_template = self.message_box.toPlainText()
        if len(message_template) == 0:
            self.showdialog(message='Message cannot be empty', dialog_type='error')
            return

        from whatsapp import main


        status_code, error_line_count_list = main(input_file_path=self.input_file_path, image_file_path=self.image_file_path,
                           failed_file_path=None,
                           message_template=message_template)

        if status_code == 0:
            self.showdialog(message='Succesfully Completed\nCheck failed.csv for failed messages.', dialog_type='alert')
        elif status_code == 1:
            message = 'Please download the appropriate version of the chrome driver from ' \
                      'https://chromedriver.chromium.org/downloads .\nAfter downloading, place the file in the ' \
                      'appropriate sub folder in the folder [chromedrivers]. '
            self.showdialog(message=message, dialog_type='error')
        elif status_code == 2:
            self.showdialog(message='Error.', dialog_type='error')
        elif status_code == 3:
            self.showdialog(message='Input csv File does not exist!', dialog_type='error')
        elif status_code == 4:
            self.showdialog(message='Image File does not exist!', dialog_type='error')
        elif status_code == 5:
            self.showdialog(message='Check your internet connection!', dialog_type='error')
        elif status_code == 6:
            error_line_count_list = ', '.join(str(x) for x in error_line_count_list)
            message = "Please make sure that phone numbers entered are valid or are in use.\nThe phone numbers " \
                      "found at line(s) " + error_line_count_list + ' are not in valid format'
            self.showdialog(message=message, dialog_type='error')
        elif status_code == 7:
            self.showdialog(message="File dos not contain any contacts.", dialog_type='error')
        else:
            self.showdialog(message='Error!', dialog_type='error')

    @pyqtSlot()
    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if self.sender() is self.select_input_file:
            filter = "csv(*.csv)"
        elif self.sender() is self.select_image:
            filter = "Image Files (*.png *.jpg)"
        file, _ = QFileDialog.getOpenFileName(self, filter=filter, options=options)
        if file:
            if self.sender() is self.select_input_file:
                print('Selected input file: ' + file)
                self.selected_input_file_label.setText(file)
                self.input_file_path = file
            elif self.sender() is self.select_image:
                print('Selected image file: ' + file)
                self.selected_image_label.setText(file)
                self.image_file_path = file

    @pyqtSlot()
    def showdialog(self, message, dialog_type='alert'):
        dialog = QMessageBox()
        if dialog_type == 'alert':
            dialog.setIcon(QMessageBox.Information)
        if dialog_type == 'error':
            dialog.setIcon(QMessageBox.Warning)
        dialog.setText(message)
        dialog.setWindowTitle(dialog_type.title())
        dialog.setStandardButtons(QMessageBox.Ok)

        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
