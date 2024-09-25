from PyQt5.QtWidgets import (QMainWindow, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout,
                             QHBoxLayout, QWidget, QLabel, QDialog, QTextEdit, QMessageBox)
from db_ini import get_connection
from my_posts import MyPosts
from design import homegape


class PostYozish(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Post yozish oynasi")

        self.setGeometry(400, 300, 600, 600)

        vertikal = QVBoxLayout()

        self.post = QTextEdit()
        self.post.setPlaceholderText("Yangi post")

        vertikal.addWidget(self.post)

        garizontal = QHBoxLayout()

        btn = QPushButton("Postni joylash")
        garizontal.addWidget(btn)
        btn.clicked.connect(self.accept)

        btn2 = QPushButton("Ortga qaytish")
        garizontal.addWidget(btn2)
        btn2.clicked.connect(self.reject)

        vertikal.addLayout(garizontal)

        self.setLayout(vertikal)
        self.setStyleSheet(homegape)

    def get_value(self):
        return self.post.toPlainText()


class HomePage(QMainWindow):
    def __init__(self, username):
        super().__init__()

        self.postlarim_oyna = None
        self.yangi_post = None

        self.username = username

        self.setWindowTitle("Twitter home page")

        self.list = QListWidget()

        vertikal = QVBoxLayout()
        garizontal = QHBoxLayout()

        new_post = QPushButton("Yangi post yozish")
        garizontal.addWidget(new_post)
        new_post.clicked.connect(self.new_post)

        postlarim = QPushButton("Mening postlarim")
        postlarim.clicked.connect(self.postlarim)
        garizontal.addWidget(postlarim)

        self.yangilash()

        vertikal.addLayout(garizontal)
        vertikal.addWidget(self.list)

        widget = QWidget()
        widget.setLayout(vertikal)
        self.setCentralWidget(widget)
        self.setStyleSheet(homegape)

    def malumot_olish(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""select * from posts order by vaqt desc;""")

        data = cur.fetchall()

        cur.close()
        conn.close()

        return data

    def yangilash(self):
        self.list.clear()
        data = self.malumot_olish()

        for malumot in data:
            item = QListWidgetItem()
            widget = QWidget()
            layout = QVBoxLayout()

            username = QLabel("user: " + malumot[1] + "\n")
            layout.addWidget(username)

            post = QLabel(malumot[2] + "\n")
            layout.addWidget(post)

            vaqt = QLabel(str(malumot[3]) + "\n")
            layout.addWidget(vaqt)

            widget.setLayout(layout)

            item.setSizeHint(widget.sizeHint())

            self.list.addItem(item)

            self.list.setItemWidget(item, widget)

    def postlarim(self):
        self.postlarim_oyna = MyPosts(self.username, self)
        self.postlarim_oyna.showMaximized()
        self.hide()

    def new_post(self):
        self.yangi_post = PostYozish()

        if self.yangi_post.exec_() == QDialog.Accepted:
            data = self.yangi_post.get_value()

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""insert ignore into posts(username, post) values (%s,%s);""", (self.username, data))

            conn.commit()

            self.yangilash()

            cur.close()
            conn.close()

            QMessageBox.information(self, "Muvaffaqiyatli", "Post mucaffaqiyatli yuklandi")
