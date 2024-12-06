from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import os
import logging
from choisir_action import Ui_Main_Menu

class Ui_DeleteProduct(object):
    def setupUi(self, Dialog, username=None, status=None):
        self.Dialog = Dialog
        self.username = username
        self.status = status
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        Dialog.setObjectName("Dialog")
        Dialog.resize(670, 500)
        Dialog.setMinimumSize(QtCore.QSize(670, 500))
        Dialog.setMaximumSize(QtCore.QSize(670, 500))

        # Définition du background
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(-130, -50, 831, 581))
        self.label.setPixmap(QtGui.QPixmap("./new/Pictures/fond.png"))
        self.label.setObjectName("background")

        # Définition du champ de texte pour l'ID
        self.id_input = QtWidgets.QLineEdit(parent=Dialog)
        self.id_input.setGeometry(QtCore.QRect(260, 110, 151, 31))
        self.id_input.setObjectName("id_input")

        # Définition du bouton de validation
        self.delete_button = QtWidgets.QPushButton(parent=Dialog)
        self.delete_button.setGeometry(QtCore.QRect(280, 160, 111, 41))
        self.delete_button.setObjectName("delete_button")

        # Définition du bouton de retour
        self.retour_button = QtWidgets.QPushButton(parent=Dialog)
        self.retour_button.setGeometry(QtCore.QRect(200, 310, 111, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./new/Pictures/icone 2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.retour_button.setIcon(icon)
        self.retour_button.setObjectName("retour_button")

        # Définition du bouton arrêtant le programme
        self.quit_button = QtWidgets.QPushButton(parent=Dialog)
        self.quit_button.setGeometry(QtCore.QRect(360, 310, 111, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./new/Pictures/icone.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.quit_button.setIcon(icon1)
        self.quit_button.setObjectName("quit_button")

        # Définition du label d'erreur
        self.id_error = QtWidgets.QLabel(parent=Dialog)
        self.id_error.setGeometry(QtCore.QRect(260, 138, 151, 15))
        self.id_error.setStyleSheet("color: red; font-size: 10px;")
        self.id_error.hide()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Connexion des boutons
        self.delete_button.clicked.connect(self.handle_delete_product)
        self.retour_button.clicked.connect(self.handle_retour)
        self.quit_button.clicked.connect(self.handle_quit)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Supprimer un produit"))
        self.id_input.setPlaceholderText(_translate("Dialog", "ID du produit"))
        self.delete_button.setText(_translate("Dialog", "Supprimer"))
        self.retour_button.setText(_translate("Dialog", " Retour"))
        self.quit_button.setText(_translate("Dialog", " Quitter"))

    def handle_delete_product(self):
        try:
            id_text = self.id_input.text()
            
            if not id_text:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.id_input.setStyleSheet(error_style)
                self.id_error.setText("L'ID ne peut pas être vide")
                self.id_error.show()
                return
            
            try:
                id = int(id_text)
            except ValueError:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.id_input.setStyleSheet(error_style)
                self.id_error.setText("L'ID doit être un nombre")
                self.id_error.show()
                return

            # Utiliser le chemin correct pour la base de données
            db_path = os.path.join(os.path.dirname(__file__), 'database.db')
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()

            # Vérifier si le produit existe
            curseur.execute("SELECT COUNT(*) FROM catalogue WHERE id = ?", (id,))
            count = curseur.fetchone()[0]

            if count == 0:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.id_input.setStyleSheet(error_style)
                self.id_error.setText("Produit non trouvé")
                self.id_error.show()
                return

            # Demander confirmation
            reply = QtWidgets.QMessageBox.question(
                self.Dialog,
                "Confirmation",
                f"Êtes-vous sûr de vouloir supprimer le produit avec l'ID {id} ?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                # Supprimer le produit
                curseur.execute("DELETE FROM catalogue WHERE id = ?", (id,))
                connection.commit()

                QtWidgets.QMessageBox.information(
                    self.Dialog,
                    "Succès",
                    "Le produit a été supprimé avec succès !"
                )

                self.logger.info(f"Produit supprimé. ID : {id}")

                # Retour au menu principal
                from choisir_action import Ui_Main_Menu
                self.window = QtWidgets.QDialog()
                self.ui = Ui_Main_Menu()
                self.ui.setupUi(self.window, self.username, self.status)
                self.Dialog.close()
                self.window.show()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Erreur de base de données",
                str(e)
            )
            self.logger.warning(f"{str(e)}")
            return

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Erreur inattendue",
                str(e)
            )
            self.logger.exception(f"{str(e)}")
            return

        finally:
            if 'connection' in locals():
                connection.close()

    def handle_retour(self):
        try:
            self.logger.info("Retour au menu principal (choisir_action.py) depuis la suppression du produit (delete_product.py)")
            from choisir_action import Ui_Main_Menu
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Main_Menu()
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

    def handle_quit(self):
        self.logger.info("Arrêt du programme")
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_DeleteProduct()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
