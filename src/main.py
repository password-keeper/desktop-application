from PyQt5.QtWidgets import QWidget, QLineEdit, QGroupBox, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel, QListWidget, QApplication
from string import ascii_lowercase, ascii_uppercase, digits
from random import choices
from sys import argv
import api

qss = "QWidget {background-color: #23272A;color: white;}QPushButton {background-color: #610094;color: white;border-style: outset;border-radius: 3px;font: 20px;padding: 3px;}QGroupBox {color: white;}QLineEdit {padding: 10px;border: 1px solid white;border-radius: 3px;color: white;}QListWidget {border: 1px solid white;border-radius: 3px;color: white;font: 17px;}QListWidget::item {padding: 5px}"
token = ""

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(600, 300)
    def initUI(self):
        group1 = QGroupBox("Sign up")
        self.name = QLineEdit()
        self.lastname = QLineEdit()
        self.email = QLineEdit()
        self.sifre = QLineEdit()
        self.buton = QPushButton("Sign up")

        group2 = QGroupBox("Log in")
        self.email2 = QLineEdit()
        self.sifre2 = QLineEdit()
        self.buton2 = QPushButton("Log in")

        self.name.setPlaceholderText("Name")
        self.lastname.setPlaceholderText("Lastname")
        self.email.setPlaceholderText("E-mail")
        self.sifre.setPlaceholderText("Password")
        self.sifre.setEchoMode(QLineEdit.Password)
        self.email2.setPlaceholderText("E-mail")
        self.sifre2.setPlaceholderText("Password")
        self.sifre2.setEchoMode(QLineEdit.Password)

        ml = QHBoxLayout()
        ml.addWidget(group1)
        ml.addWidget(group2)

        kl = QVBoxLayout()
        kl.addWidget(self.name)
        kl.addWidget(self.lastname)
        kl.addWidget(self.email)
        kl.addWidget(self.sifre)
        kl.addStretch()
        kl.addWidget(self.buton)
        group1.setLayout(kl)

        gl = QVBoxLayout()
        gl.addWidget(self.email2)
        gl.addWidget(self.sifre2)
        gl.addStretch()
        gl.addWidget(self.buton2)
        group2.setLayout(gl)

        ml.addLayout(kl)

        self.setLayout(ml)
        self.setStyleSheet(qss)
        self.show()

        self.buton.clicked.connect(self.kayit)
        self.buton2.clicked.connect(self.oturum)

    def kayit(self):
        if self.name.text() == "" or self.lastname.text() == "" or self.email.text() == "" or self.sifre.text() == "":
            QMessageBox.critical(self, "Password Manager", "Please fill the all blanks.")
        else:
            a = api.signup(self.name.text(), self.lastname.text(), self.email.text(), self.sifre.text())
            if a == False:
                QMessageBox.critical(self, "Password Manager", "Sign up failed.")
            else:
                QMessageBox.information(self, "Password Manager", "Sign up was successful.")

    def oturum(self):
        if self.email2.text() == "" or self.sifre2.text() == "":
            QMessageBox.critical(self, "Password Manager", "Please fill the all blanks.")
        else:
            a = api.login(self.email2.text(), self.sifre2.text())
            if a == False:
                QMessageBox.critical(self, "Password Manager", "Log in failed.")
            else:
                QMessageBox.information(self, "Password Manager", "Log in was successful.")
                globals()['token'] = a
                self.login = Sifreler()
                self.login.show()
                self.close()

class SifreEkle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Password Manager - Add Password")
        self.setFixedSize(500, 200)
    def initUI(self):
        self.isim = QLineEdit()
        self.isim.setPlaceholderText("Password Name")
        self.sifre = QLineEdit()
        self.sifre.setPlaceholderText("Password")
        rastbuton = QPushButton("🎲")
        rastbuton.setStyleSheet("padding: 9px")
        buton = QPushButton("Submit")
        self.text = QLabel()

        hb = QHBoxLayout()
        hb.addWidget(self.sifre)
        hb.addWidget(rastbuton)

        vb = QVBoxLayout()
        vb.addWidget(self.isim)
        vb.addLayout(hb)
        vb.addStretch()
        vb.addWidget(buton)
        
        buton.clicked.connect(self.ekle)
        rastbuton.clicked.connect(self.randomg)

        self.setLayout(vb)
        self.setStyleSheet(qss)
        self.show()

    def ekle(self):
        if self.isim.text() == "" or self.sifre.text() == "":
            QMessageBox.critical(self, "Password Manager", "Please fill the all blanks.")
        else:
            a = api.addPassword(token, self.isim.text(), self.sifre.text())
            if a == True:
                QMessageBox.information(self, "Password Manager", "Password successfully added.")
            else:
                QMessageBox.critical(self, "Password Manager", "Couldn't add password.")

    def randomg(self):
        rastgele = ''.join(choices(ascii_lowercase + ascii_uppercase + digits, k = 16))
        self.sifre.setText(rastgele)

class SifreDuzenle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Password Manager - Edit Password")
        self.setFixedSize(500, 200)
    def initUI(self):
        self.isim1 = QLineEdit()
        self.isim1.setPlaceholderText("Old Password Name")
        self.isim = QLineEdit()
        self.isim.setPlaceholderText("New Password Name")
        self.sifre = QLineEdit()
        self.sifre.setPlaceholderText("New Password")
        buton = QPushButton("Submit")
        self.text = QLabel()

        vb = QVBoxLayout()
        vb.addWidget(self.isim1)
        vb.addWidget(self.isim)
        vb.addWidget(self.sifre)
        vb.addStretch()
        vb.addWidget(buton)
        
        buton.clicked.connect(self.duzen)

        self.setLayout(vb)
        self.setStyleSheet(qss)
        self.show()

    def duzen(self):
        if self.isim.text() == "" or self.sifre.text() == "":
            QMessageBox.critical(self, "Password Manager", "Please fill the all blanks.")
        else:
            a = api.editPassword(token, self.isim1.text() ,self.isim.text(), self.sifre.text())
            if a == True:
                QMessageBox.information(self, "Password Manager", "Password set successfully.")
            else:
                QMessageBox.critical(self, "Password Manager", "Couldn't edit password.")

class SifreSil(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Password Manager - Delete Password")
        self.setFixedSize(500, 100)
    def initUI(self):
        self.isim = QLineEdit()
        self.isim.setPlaceholderText("Password Name")
        buton = QPushButton("Submit")
        self.text = QLabel()

        vb = QVBoxLayout()
        vb.addWidget(self.isim)
        vb.addStretch()
        vb.addWidget(buton)
        
        buton.clicked.connect(self.sil)

        self.setLayout(vb)
        self.setStyleSheet(qss)
        self.show()

    def sil(self):
        if self.isim.text() == "":
            QMessageBox.critical(self, "Password Manager", "Please fill the all blanks.")
        else:
            a = api.deletePassword(token, self.isim.text())
            if a == True:
                QMessageBox.information(self, "Password Manager", "Password deleted successfully.")
            else:
                QMessageBox.critical(self, "Password Manager", "Couldn't delete password.")

class Sifreler(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(300, 500)
    def initUI(self):
        self.liste = QListWidget()
        buton = QPushButton("+")
        buton2 = QPushButton("⟳")
        buton3 = QPushButton("-")
        buton4 = QPushButton("Refresh")

        hb = QHBoxLayout()
        hb.addWidget(buton)
        hb.addWidget(buton2)
        hb.addWidget(buton3)

        vb = QVBoxLayout()
        vb.addLayout(hb)
        vb.addWidget(self.liste)
        vb.addWidget(buton4)

        self.liste.itemDoubleClicked.connect(self.test)
        buton.clicked.connect(self.ekle)
        buton2.clicked.connect(self.duzenle)
        buton3.clicked.connect(self.sil)
        buton4.clicked.connect(self.yenile)

        self.setLayout(vb)
        self.setStyleSheet(qss)
        self.show()

        self.yenile()

    def test(self, item):
        QMessageBox.information(self, "Password Manager", f"Password Name: {item.text()}\nPassword: {api.getPasswordByName(token, item.text())}")
    
    def ekle(self):
        self.ekle = SifreEkle()
        self.ekle.show()

    def duzenle(self):
        self.duzenle = SifreDuzenle()
        self.duzenle.show()

    def sil(self):
        self.sil = SifreSil()
        self.sil.show()

    def yenile(self):
        try:
            passwords = api.getAllPasswords(token)
            self.liste.clear()
            for i in passwords:
                self.liste.addItem(i)
        except:
            self.liste.addItem("Clean.")

app = QApplication(argv)
w = Main()
w.show()
app.exec()

# larei & forcex was here
