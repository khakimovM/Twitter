from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from components import spacer
from regitratsiya import Registratsiya
from db_ini import get_connection
from home_page import HomePage
from design import login_reg


class LoginRegistr(QMainWindow):
    def __init__(self):
        super().__init__()

        self.registr_oyna = None
        self.yangi_oyna = None

        self.setWindowTitle("Twitter login")

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        vertikal.addItem(spacer())

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        vertikal.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        vertikal.addWidget(self.password)

        btn = QPushButton("Kirish")
        btn.clicked.connect(self.kirishga_ot)
        vertikal.addWidget(btn)

        btn2 = QPushButton("Registratsiya")
        btn2.clicked.connect(self.registrga_ot)
        vertikal.addWidget(btn2)

        vertikal.addItem(spacer())

        garizontal.addItem(spacer())
        garizontal.addLayout(vertikal)
        garizontal.addItem(spacer())

        widget = QWidget()
        widget.setLayout(garizontal)
        self.setCentralWidget(widget)
        self.setStyleSheet(login_reg)

    def kirishga_ot(self):
        username = self.username.text()
        password = self.password.text()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select * from users where username=%s and password=%s""", (username, password))

        data = cur.fetchone()

        if data:
            self.yangi_oyna = HomePage(username)
            self.yangi_oyna.showMaximized()
            self.close()
        else:
            QMessageBox.warning(self, "Ogohlantirish", "Siz kiritgan user yoki password xato")

    def registrga_ot(self):
        self.registr_oyna = Registratsiya(self)
        self.registr_oyna.showMaximized()
        self.hide()

