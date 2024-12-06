from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import os
import hashlib
import logging
from login import Ui_Login
from password_verification import check_password_security, generate_password

class Ui_Register(object):
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

        # Définition du champ de texte pour la confirmation du mot de passe
        self.confirm_password_input = QtWidgets.QLineEdit(parent=self.Dialog)
        self.confirm_password_input.setGeometry(QtCore.QRect(260, 210, 151, 31))
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_password_input.setObjectName("confirm_password_input")

        # Définition du bouton d'inscription
        self.register_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.register_button.setGeometry(QtCore.QRect(280, 260, 111, 41))
        self.register_button.setObjectName("register_button")

        # Définition du bouton de retour
        self.back_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.back_button.setGeometry(QtCore.QRect(280, 310, 111, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./new/Pictures/icone 2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.back_button.setIcon(icon)
        self.back_button.setObjectName("back_button")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

        # Connexion des boutons
        self.register_button.clicked.connect(self.handle_register)
        self.back_button.clicked.connect(self.handle_back)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Inscription"))
        self.username_input.setPlaceholderText(_translate("Dialog", "Nom d'utilisateur"))
        self.password_input.setPlaceholderText(_translate("Dialog", "Mot de passe"))
        self.confirm_password_input.setPlaceholderText(_translate("Dialog", "Confirmer le mot de passe"))
        self.register_button.setText(_translate("Dialog", "S'inscrire"))
        self.back_button.setText(_translate("Dialog", " Retour"))

    def handle_register(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()

            if not username or not password or not confirm_password:
                QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur",
                    "Veuillez remplir tous les champs."
                )
                return

            if password != confirm_password:
                QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur",
                    "Les mots de passe ne correspondent pas."
                )
                return

            # Vérification de la sécurité du mot de passe
            is_secure, message = check_password_security(password)
            if not is_secure:
                # Si le mot de passe est compromis, proposer un mot de passe généré
                reply = QtWidgets.QMessageBox()
                reply.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                reply.setWindowTitle("Mot de passe non sécurisé")
                reply.setText(message)
                reply.setInformativeText("Voulez-vous utiliser un mot de passe généré aléatoirement ?")
                reply.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes |
                    QtWidgets.QMessageBox.StandardButton.No
                )
                reply.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Yes)
                
                if reply.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    # Générer et afficher un nouveau mot de passe
                    new_password = generate_password()
                    self.password_input.setText(new_password)
                    self.confirm_password_input.setText(new_password)
                    QtWidgets.QMessageBox.information(
                        self.Dialog,
                        "Nouveau mot de passe",
                        f"Votre nouveau mot de passe est : {new_password}\nVeuillez le noter en lieu sûr."
                    )
                return

            # Hachage du mot de passe
            hashed_password = hashlib.sha256(password.encode('UTF-8')).hexdigest().upper()

            # Connexion à la base de données
            db_path = os.path.join(os.path.dirname(__file__), 'database.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Vérifier si l'utilisateur existe déjà
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            if cursor.fetchone() is not None:
                QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur",
                    "Ce nom d'utilisateur est déjà pris."
                )
                return

            # Demander confirmation
            reply = QtWidgets.QMessageBox.question(
                self.Dialog,
                "Confirmation",
                "Voulez-vous vraiment créer ce compte ?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                # Insérer le nouvel utilisateur
                cursor.execute("INSERT INTO users (username, password, status) VALUES (?, ?, 'user')", (username, hashed_password))
                conn.commit()

                QtWidgets.QMessageBox.information(
                    self.Dialog,
                    "Succès",
                    "Inscription réussie! Vous pouvez maintenant vous connecter."
                )

                # Redirection vers la page de connexion
                self.logger.info(f"Nouvel utilisateur inscrit : {username}")
                self.window = QtWidgets.QDialog()
                self.ui = Ui_Login()
                self.ui.setupUi(self.window)
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

    def handle_back(self):
        try:
            self.logger.info("Retour à la page de connexion")
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Login()
            self.ui.setupUi(self.window)
            self.Dialog.close()
            self.window.show()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Erreur inattendue",
                str(e)
            )
            self.logger.exception(f"{str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Register()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec()) 