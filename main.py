from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore
from pymongo import MongoClient
import login
import register
import bcrypt
import sys

file = open('dbpass.txt', 'r')
dbpass = file.read()
client = MongoClient(f'mongodb+srv://<username>:{dbpass}@<username>.pse2r.mongodb.net/?retryWrites=true&w=majority')
db = client['Login']


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = login.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.pushButton.clicked.connect(lambda: self.close())
        self.ui.pushButton_2.clicked.connect(lambda: self.showMinimized())
        self.ui.pushButton_3.clicked.connect(self.maximize)
        self.ui.pushButton_4.clicked.connect(self.login)
        self.ui.pushButton_5.clicked.connect(self.register)

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text().encode('utf-8')
        find = db["Users"].find_one({"username": username})

        try:
            findpass = find["password"]

        except:
            self.ui.label_3.setText('Login Unsuccessful :(')

        if bcrypt.checkpw(password, findpass):
            self.ui.label_3.setText('Login Successful :)')


    def maximize(self):
        pass

    def register(self):
        self.re = RegisterWindow()
        self.re.show()

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.re = register.Ui_MainWindow()
        self.re.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.re.pushButton.clicked.connect(lambda: self.close())
        self.re.pushButton_2.clicked.connect(lambda: self.showMinimized())
        self.re.pushButton_3.clicked.connect(self.maximize)
        self.re.pushButton_5.clicked.connect(self.login)
        self.re.pushButton_4.clicked.connect(self.register)

    def maximize(self):
        pass

    def register(self):
        username = self.re.lineEdit.text()
        password = self.re.lineEdit_2.text()
        verify = self.re.lineEdit_3.text()
        salt = bcrypt.gensalt()

        if username == "" or password == "" or verify == "":
            self.re.label_3.setText("You are missing requirements")

        if password == verify:
            password = password.encode('utf-8')
            hashedpass = bcrypt.hashpw(password, salt)
            account = {"username": username, "password": hashedpass}
            db["Users"].insert_one(account)
            self.re.label_3.setText('Successfully Registered')

    def login(self):
        self.ui = MainWindow()
        self.ui.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MyWindow = MainWindow()
    MyWindow.show()
    sys.exit(app.exec_())