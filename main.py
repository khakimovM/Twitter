from PyQt5.QtWidgets import QApplication
from login_registratsiya import LoginRegistr
from db_ini import load_tables


app = QApplication([])

load_tables()
kirish = LoginRegistr()
kirish.showMaximized()

app.exec_()
