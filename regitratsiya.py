from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from components import spacer
from db_ini import get_connection
from home_page import HomePage
from design import login_reg


class Registratsiya(QMainWindow):
    def __init__(self, bosh_oyna):
        super().__init__()

        self.bosh_oyna = bosh_oyna

        self.yaangi_oyna = None

        self.setWindowTitle("Twitter Registratsiya")

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        vertikal.addItem(spacer())

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        vertikal.addWidget(self.name)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        vertikal.addWidget(self.username)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        vertikal.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        vertikal.addWidget(self.password)

        ichki_garizontal = QHBoxLayout()

        kirish = QPushButton("Kirish")
        kirish.clicked.connect(self.bosildi)
        ichki_garizontal.addWidget(kirish)

        ortga = QPushButton("Ortga qaytish")
        ortga.clicked.connect(self.ortga_qayt)
        ichki_garizontal.addWidget(ortga)

        vertikal.addLayout(ichki_garizontal)

        vertikal.addItem(spacer())

        garizontal.addItem(spacer())
        garizontal.addLayout(vertikal)
        garizontal.addItem(spacer())

        widget = QWidget()
        widget.setLayout(garizontal)
        self.setCentralWidget(widget)
        self.setStyleSheet(login_reg)

    def ortga_qayt(self):
        self.bosh_oyna.showMaximized()
        self.close()

    def bosildi(self):
        name = self.name.text()
        username = self.username.text()
        email = self.email.text()
        password = self.password.text()

        if len(name) > 0 and len(username) > 0 and '@gmail.com' in email and len(password) > 0:
            try:
                conn = get_connection()
                cur = conn.cursor()

                cur.execute("""insert into users(name,username,email,password) values
                    (%s,%s,%s,%s);
                """, (name, username, email, password))

                conn.commit()

                cur.close()
                conn.close()

                QMessageBox.information(self, "Muvaffaqiyatli", "Siz tizimga muvaffaqiyatli ulandingiz")

                self.yaangi_oyna = HomePage(username)
                self.yaangi_oyna.showMaximized()
                self.close()

            except:
                QMessageBox.warning(self, "Ogohlantirish", "Siz kiritgan username band qilingan")
        else:
            QMessageBox.warning(self, "Ogohlantirish", "Siz ma'lumotlarni to'liq kiritmadingiz")
