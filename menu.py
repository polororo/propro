from PyQt6 import QtCore, QtGui, QtWidgets
import logging

class Ui_Menu(object):
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

        self.titre_ecrit = QtWidgets.QLabel(parent=self.Dialog)
        self.titre_ecrit.setGeometry(QtCore.QRect(250, 70, 300, 25))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(16)
        self.titre_ecrit.setFont(font)
        self.titre_ecrit.setStyleSheet("color: rgb(255, 255, 255);")
        self.titre_ecrit.setObjectName("titre_ecrit")

        # Définition du bouton de connexion
        self.connexion_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.connexion_button.setGeometry(QtCore.QRect(215, 200, 111, 41))
        self.connexion_button.setObjectName("connexion_button")

        # Définition du bouton redirigeant vers le menu principal en tant qu'invité
        self.invite_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.invite_button.setGeometry(QtCore.QRect(345, 200, 111, 41))
        self.invite_button.setObjectName("invite_button")
        
        # Définition du bouton de création de compte
        self.account_creation_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.account_creation_button.setGeometry(QtCore.QRect(280, 260, 111, 41))
        self.account_creation_button.setObjectName("account_creation_button")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

        # Connexion des boutons aux fonctions
        self.connexion_button.clicked.connect(self.handle_button_1)
        self.invite_button.clicked.connect(self.handle_button_2)
        self.account_creation_button.clicked.connect(self.handle_button_3)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Menu de connexion"))
        self.connexion_button.setText(_translate("Dialog", "Se connecter"))
        self.invite_button.setText(_translate("Dialog", "Invité"))
        self.account_creation_button.setText(_translate("Dialog", "Créer un compte"))
        self.titre_ecrit.setText(_translate("Dialog", "Menu de connexion"))

    def handle_button_1(self):
        try:
            self.logger.info("Appel de la page de connexion (login.py) depuis le menu de connexion (menu.py)")
            from login import Ui_Login
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

    def handle_button_2(self):
        try:
            self.logger.info("Appel de la page du menu principal (choisir_action.py) en tant qu'invité depuis le menu de connexion (menu.py)")
            from choisir_action import Ui_Main_Menu
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Main_Menu()
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

    def handle_button_3(self):
        try:
            self.logger.info("Appel de la page de création de compte (sign_up.py) depuis le menu de connexion (menu.py)")
            from sign_up import Sign_Up
            self.window = QtWidgets.QDialog()
            self.ui = Sign_Up()
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
    try:


        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Menu()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec())

    except Exception as e:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger.exception(f"{str(e)}")