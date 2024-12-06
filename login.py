from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import os
import pyotp
import logging
import hashlib
from choisir_action import Ui_Main_Menu

class Ui_Login(object):
    def setupUi(self, Dialog):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(670, 500)
        self.Dialog.setMinimumSize(QtCore.QSize(670, 500))
        self.Dialog.setMaximumSize(QtCore.QSize(670, 500))

        # Définition du background
        self.label = QtWidgets.QLabel(parent=self.Dialog)
        self.label.setGeometry(QtCore.QRect(-130, -50, 831, 581))
        self.label.setPixmap(QtGui.QPixmap("./new/Pictures/fond.png"))
        self.label.setObjectName("background")

        # Définition du champ de texte pour le nom d'utilisateur
        self.username_input = QtWidgets.QLineEdit(parent=self.Dialog)
        self.username_input.setGeometry(QtCore.QRect(260, 110, 151, 31))
        self.username_input.setObjectName("username_input")

        # Définition du champ de texte pour le mot de passe
        self.password_input = QtWidgets.QLineEdit(parent=self.Dialog)
        self.password_input.setGeometry(QtCore.QRect(260, 160, 151, 31))
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("password_input")

        # Définition du champ pour le code 2FA
        self.twofa_input = QtWidgets.QLineEdit(parent=self.Dialog)
        self.twofa_input.setGeometry(QtCore.QRect(260, 210, 151, 31))
        self.twofa_input.setObjectName("twofa_input")

        # Définition du bouton de connexion
        self.login_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.login_button.setGeometry(QtCore.QRect(280, 260, 111, 41))
        self.login_button.setObjectName("login_button")

        # Définition du bouton arrêtant le programme
        self.quit_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.quit_button.setGeometry(QtCore.QRect(280, 310, 111, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./new/Pictures/icone.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.quit_button.setIcon(icon)
        self.quit_button.setObjectName("quit_button")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

        # Connexion des boutons
        self.login_button.clicked.connect(self.handle_login)
        self.quit_button.clicked.connect(self.handle_quit)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Connexion"))
        self.username_input.setPlaceholderText(_translate("Dialog", "Nom d'utilisateur"))
        self.password_input.setPlaceholderText(_translate("Dialog", "Mot de passe"))
        self.twofa_input.setPlaceholderText(_translate("Dialog", "Code 2FA"))
        self.login_button.setText(_translate("Dialog", "Connexion"))
        self.quit_button.setText(_translate("Dialog", " Quitter"))

    def handle_login(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            twofa_code = self.twofa_input.text()

            # Hachage du mot de passe
            hashed_password = hashlib.sha256(password.encode('UTF-8')).hexdigest().upper()

            if not username or not password:
                QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur",
                    "Veuillez remplir tous les champs."
                )
                return

            # Connexion à la base de données
            db_path = os.path.join(os.path.dirname(__file__), 'database.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Vérification des identifiants
            cursor.execute("SELECT password, otp_secret, status FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result is None:
                QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur",
                    "Nom d'utilisateur ou mot de passe incorrect."
                )
                return

            stored_password, otp_secret, status = result

            if hashed_password != stored_password:
                QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur",
                    "Nom d'utilisateur ou mot de passe incorrect."
                )
                return

            # Vérification du code 2FA si configuré
            if otp_secret:
                if not twofa_code:
                    QtWidgets.QMessageBox.warning(
                        self.Dialog,
                        "Erreur",
                        "Code 2FA requis."
                    )
                    return

                totp = pyotp.TOTP(otp_secret)
                if not totp.verify(twofa_code):
                    QtWidgets.QMessageBox.warning(
                        self.Dialog,
                        "Erreur",
                        "Code 2FA invalide."
                    )
                    return

            # Connexion réussie, ouverture du menu principal
            self.logger.info(f"Connexion réussie pour l'utilisateur {username}")
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Main_Menu()
            self.ui.setupUi(self.window, username, status)
            self.Dialog.close()
            self.window.show()

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Erreur inattendue",
                str(e)
            )
            self.logger.exception(f"{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def handle_quit(self):
        self.logger.info("Arrêt du programme")
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())