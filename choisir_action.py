from PyQt6 import QtCore, QtGui, QtWidgets
import logging


class Ui_Main_Menu(object):
    def setupUi(self, Dialog, username=None, status=None):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(670, 500)
        self.Dialog.setMinimumSize(QtCore.QSize(670, 500))
        self.Dialog.setMaximumSize(QtCore.QSize(670, 500))
        
        self.username = username
        self.status = status

        self.label = QtWidgets.QLabel(parent=self.Dialog)
        self.label.setGeometry(QtCore.QRect(-130, -50, 831, 581))
        self.label.setPixmap(QtGui.QPixmap("./new/Pictures/fond.png"))
        self.label.setObjectName("background")

        self.afficher_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.afficher_button.setGeometry(QtCore.QRect(280, 110, 111, 41))
        self.afficher_button.setObjectName("afficher_button")

        self.creer_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.creer_button.setGeometry(QtCore.QRect(280, 160, 111, 41))
        self.creer_button.setObjectName("creer_button")
        self.creer_button.setVisible(status == "admin")

        self.modifier_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.modifier_button.setGeometry(QtCore.QRect(280, 210, 111, 41))
        self.modifier_button.setObjectName("modifier_button")
        self.modifier_button.setVisible(status in ["admin", "editor"])

        self.supprimer_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.supprimer_button.setGeometry(QtCore.QRect(280, 260, 111, 41))
        self.supprimer_button.setObjectName("supprimer_button")
        self.supprimer_button.setVisible(status == "admin")

        self.status_label = QtWidgets.QLabel(parent=self.Dialog)
        self.status_label.setGeometry(QtCore.QRect(10, 10, 200, 30))
        self.status_label.setStyleSheet("color: white; font-size: 12px;")
        self.status_label.setText(f"Connecté en tant que : {username}\nStatut : {status}")

        self.retour_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.retour_button.setGeometry(QtCore.QRect(200, 310, 111, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./new/Pictures/icone 2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.retour_button.setIcon(icon)
        self.retour_button.setObjectName("retour_button")

        self.quit_button = QtWidgets.QPushButton(parent=self.Dialog)
        self.quit_button.setGeometry(QtCore.QRect(360, 310, 111, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./new/Pictures/icone.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.quit_button.setIcon(icon1)
        self.quit_button.setObjectName("quit_button")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        
        # Connexion des boutons
        self.afficher_button.clicked.connect(self.handle_afficher)
        self.creer_button.clicked.connect(self.handle_creer)
        self.modifier_button.clicked.connect(self.handle_modifier)
        self.supprimer_button.clicked.connect(self.handle_supprimer)
        self.retour_button.clicked.connect(self.handle_retour)
        self.quit_button.clicked.connect(self.handle_quit)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Menu Principal"))
        self.afficher_button.setText(_translate("Dialog", "Catalogue"))
        self.creer_button.setText(_translate("Dialog", "Créer"))
        self.modifier_button.setText(_translate("Dialog", "Modifier"))
        self.supprimer_button.setText(_translate("Dialog", "Supprimer"))
        self.retour_button.setText(_translate("Dialog", " Retour"))
        self.quit_button.setText(_translate("Dialog", " Quitter"))

    def handle_afficher(self):
        try:
            self.logger.info("Ouverture du catalogue")
            from afficher_catalogue import Ui_Catalogue
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Catalogue()
            self.ui.setupUi(self.window, self.username, self.status)
            self.Dialog.close()
            self.window.show()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")

    def handle_creer(self):
        if self.status != "admin":
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Accès refusé",
                "Seuls les administrateurs peuvent créer des produits."
            )
            return

        try:
            self.logger.info("Ouverture de la page de création de produit")
            from create_product import Ui_CreateProduct
            self.window = QtWidgets.QDialog()
            self.ui = Ui_CreateProduct()
            self.ui.setupUi(self.window, self.username, self.status)
            self.Dialog.close()
            self.window.show()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")

    def handle_modifier(self):
        if self.status not in ["admin", "editor"]:
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Accès refusé",
                "Seuls les administrateurs et les éditeurs peuvent modifier des produits."
            )
            return

        try:
            self.logger.info("Ouverture de la page de modification de produit")
            from update_product import Ui_UpdateProduct
            self.window = QtWidgets.QDialog()
            self.ui = Ui_UpdateProduct()
            self.ui.setupUi(self.window, self.username, self.status)
            self.Dialog.close()
            self.window.show()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")

    def handle_supprimer(self):
        if self.status != "admin":
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Accès refusé",
                "Seuls les administrateurs peuvent supprimer des produits."
            )
            return

        try:
            self.logger.info("Ouverture de la page de suppression de produit")
            from delete_product import Ui_DeleteProduct
            self.window = QtWidgets.QDialog()
            self.ui = Ui_DeleteProduct()
            self.ui.setupUi(self.window, self.username, self.status)
            self.Dialog.close()
            self.window.show()
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")

    def handle_retour(self):
        try:
            self.logger.info("Retour au menu de connexion")
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

    def handle_quit(self):
        self.logger.info("Arrêt du programme")
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Main_Menu()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
