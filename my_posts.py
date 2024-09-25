from PyQt5.QtWidgets import (QMainWindow, QWidget, QListWidget, QListWidgetItem, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QMessageBox, QTextEdit, QDialog)
from components import spacer, hspacer
from db_ini import get_connection
from design import mening_postlarim


class EditWindow(QDialog):
    def __init__(self, malumot):
        super().__init__()

        self.setWindowTitle("Edit oynasi")

        self.setGeometry(400, 400, 400, 300)

        vertikal = QVBoxLayout()

        self.post = QTextEdit(malumot)
        vertikal.addWidget(self.post)

        garizontal = QHBoxLayout()

        btn = QPushButton("Saqlash")
        garizontal.addWidget(btn)
        btn.clicked.connect(self.accept)

        btn2 = QPushButton("Bekor qilish")
        garizontal.addWidget(btn2)
        btn2.clicked.connect(self.reject)

        vertikal.addLayout(garizontal)

        self.setLayout(vertikal)
        self.setStyleSheet(mening_postlarim)

    def get_value(self):
        return self.post.toPlainText()


class MyPosts(QMainWindow):
    def __init__(self, username, asosiy):
        super().__init__()

        self.asosiy_oyna = asosiy
        self.username = username
        self.edit_oyna = None

        self.setWindowTitle("Mening postlarim")

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        garizontal.addItem(hspacer())

        label = QLabel("Mening postlarim")
        garizontal.addWidget(label)

        garizontal.addItem(hspacer())

        self.list = QListWidget()

        self.yangilash()

        vertikal.addLayout(garizontal)
        vertikal.addWidget(self.list)

        btn = QPushButton("Ortga qaytish")
        btn.clicked.connect(self.ortga_qayt)
        vertikal.addWidget(btn)

        widget = QWidget()
        widget.setLayout(vertikal)
        self.setCentralWidget(widget)
        self.setStyleSheet(mening_postlarim)

    def malumotni_olish(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select * from posts where username=%s order by vaqt desc;""", (self.username,))

        data = cur.fetchall()

        cur.close()
        conn.close()

        return data

    def yangilash(self):
        self.list.clear()
        data = self.malumotni_olish()

        for malumot in data:
            item = QListWidgetItem()
            widget = QWidget()
            vertikal = QVBoxLayout()
            garizontal = QHBoxLayout()

            username = QLabel(malumot[1] + "\n")
            vertikal.addWidget(username)

            post = QLabel(malumot[2] + "\n")
            vertikal.addWidget(post)

            vaqt = QLabel(str(malumot[3]) + "\n")
            vertikal.addWidget(vaqt)

            garizontal.addLayout(vertikal)
            garizontal.addItem(spacer())

            delete = QPushButton("Delete")
            delete.clicked.connect(lambda checked, post_id=malumot[0]: self.delete_bosildi(post_id))
            garizontal.addWidget(delete)

            edit = QPushButton("Edit")
            garizontal.addWidget(edit)
            edit.clicked.connect(lambda checked, post_id=malumot[0]: self.edit_bosildi(post_id))

            widget.setLayout(garizontal)

            item.setSizeHint(widget.sizeHint())

            self.list.addItem(item)

            self.list.setItemWidget(item, widget)

    def delete_bosildi(self, post_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""delete from posts where id=%s;""", (post_id,))

        conn.commit()

        cur.close()
        conn.close()

        QMessageBox.information(self, "Muvaffaqiyatli", "Post muvaffaqiyatli o'chirildi")

        self.yangilash()
        self.asosiy_oyna.yangilash()

    def ortga_qayt(self):
        self.close()
        self.asosiy_oyna.showMaximized()

    def edit_bosildi(self, post_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select post from posts where id=%s""", (post_id,))

        data = cur.fetchone()

        self.edit_oyna = EditWindow(data[0])

        if self.edit_oyna.exec_() == QDialog.Accepted:
            malumot = self.edit_oyna.get_value()
            cur.execute("""update posts set post=%s where id=%s""", (malumot, post_id))

            conn.commit()

            self.yangilash()

            QMessageBox.information(self, "Muvaffaqiyatli", "Post muvaffaqiyatli o'zgartirildi")

        cur.close()
        conn.close()
