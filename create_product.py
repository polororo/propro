from PyQt6 import QtCore, QtGui, QtWidgets
import logging
import sqlite3
import os


class Ui_CreateProduct(object):
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


        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        self.titre_ecrit = QtWidgets.QLabel(parent=Dialog)
        self.titre_ecrit.setGeometry(QtCore.QRect(250, 5, 171, 21))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(12)
        self.titre_ecrit.setFont(font)
        self.titre_ecrit.setStyleSheet("color: rgb(255, 255, 255);")
        self.titre_ecrit.setObjectName("titre_ecrit")

        self.cat_choix_nom = QtWidgets.QFrame(parent=self.frame)
        self.cat_choix_nom.setGeometry(QtCore.QRect(10, 30, 582, 90))
        self.cat_choix_nom.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.cat_choix_nom.setObjectName("cat_choix_nom")

        self.nom = QtWidgets.QLabel(parent=self.cat_choix_nom)
        self.nom.setGeometry(QtCore.QRect(10, 10, 561, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.nom.setFont(font)
        self.nom.setStyleSheet("color: rgb(255, 255, 255);")
        self.nom.setObjectName("nom")

        self.champs_nom = QtWidgets.QLineEdit(parent=self.cat_choix_nom)
        self.champs_nom.setGeometry(QtCore.QRect(10, 50, 200, 30))
        self.champs_nom.setObjectName("champs_nom")

        self.cat_choix_prix = QtWidgets.QFrame(parent=self.frame)
        self.cat_choix_prix.setGeometry(QtCore.QRect(10, 110, 582, 90))
        self.cat_choix_prix.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.cat_choix_prix.setObjectName("cat_choix_prix")

        self.prix = QtWidgets.QLabel(parent=self.cat_choix_prix)
        self.prix.setGeometry(QtCore.QRect(10, 10, 561, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.prix.setFont(font)
        self.prix.setStyleSheet("color: rgb(255, 255, 255);")
        self.prix.setObjectName("prix")

        self.champs_prix = QtWidgets.QLineEdit(parent=self.cat_choix_prix)
        self.champs_prix.setGeometry(QtCore.QRect(10, 50, 200, 30))
        self.champs_prix.setObjectName("champs_prix")

        self.cat_choix_categorie = QtWidgets.QFrame(parent=self.frame)
        self.cat_choix_categorie.setGeometry(QtCore.QRect(10, 200, 601, 80))
        self.cat_choix_categorie.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.cat_choix_categorie.setObjectName("cat_choix_categorie")

        self.categorie = QtWidgets.QLabel(parent=self.cat_choix_categorie)
        self.categorie.setGeometry(QtCore.QRect(10, 0, 561, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.categorie.setFont(font)
        self.categorie.setStyleSheet("color: rgb(255, 255, 255);")
        self.categorie.setObjectName("categorie")

        self.cat_choix_description = QtWidgets.QFrame(parent=self.cat_choix_categorie)
        self.cat_choix_description.setGeometry(QtCore.QRect(-10, 70, 582, 231))
        self.cat_choix_description.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.cat_choix_description.setObjectName("cat_choix_description")

        self.champs_categorie = QtWidgets.QLineEdit(parent=self.cat_choix_categorie)
        self.champs_categorie.setGeometry(QtCore.QRect(10, 40, 200, 30))
        self.champs_categorie.setObjectName("champs_categorie")

        self.retour_quitter = QtWidgets.QFrame(parent=self.frame)
        self.retour_quitter.setGeometry(QtCore.QRect(20, 400, 550, 80))
        self.retour_quitter.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.retour_quitter.setObjectName("retour_quitter")

        self.boutton_retour = QtWidgets.QPushButton(parent=self.retour_quitter)
        self.boutton_retour.setGeometry(QtCore.QRect(0, 40, 111, 41))
        self.boutton_retour.setObjectName("boutton_retour")
        
        self.boutton_quitter = QtWidgets.QPushButton(parent=self.retour_quitter)
        self.boutton_quitter.setGeometry(QtCore.QRect(400, 40, 111, 41))
        self.boutton_quitter.setObjectName("boutton_quitter")

        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(-14, -8, 701, 521))
        self.label.setPixmap(QtGui.QPixmap("./new/Pictures/fond.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.champs_description = QtWidgets.QLineEdit(parent=self.frame)
        self.champs_description.setGeometry(QtCore.QRect(20, 320, 300, 30))
        self.champs_description.setObjectName("champs_description")

        self.description = QtWidgets.QLabel(parent=self.frame)
        self.description.setGeometry(QtCore.QRect(20, 280, 561, 32))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.description.setFont(font)
        self.description.setStyleSheet("color: rgb(255, 255, 255);")
        self.description.setObjectName("description")

        self.boutton_valider = QtWidgets.QPushButton(parent=self.frame)
        self.boutton_valider.setGeometry(QtCore.QRect(20, 380, 111, 41))
        self.boutton_valider.setObjectName("boutton_valider")

        self.label.raise_()
        self.cat_choix_nom.raise_()
        self.cat_choix_prix.raise_()
        self.cat_choix_categorie.raise_()
        self.retour_quitter.raise_()
        self.champs_description.raise_()
        self.description.raise_()
        self.boutton_valider.raise_()

        # Définition des labels d'erreur
        self.nom_erreur = QtWidgets.QLabel(parent=self.cat_choix_nom)
        self.nom_erreur.setGeometry(QtCore.QRect(10, 78, 200, 15))
        self.nom_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.nom_erreur.hide()

        self.prix_erreur = QtWidgets.QLabel(parent=self.cat_choix_prix)
        self.prix_erreur.setGeometry(QtCore.QRect(10, 78, 200, 15))
        self.prix_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.prix_erreur.hide()
        
        self.categorie_erreur = QtWidgets.QLabel(parent=self.cat_choix_categorie)
        self.categorie_erreur.setGeometry(QtCore.QRect(10, 68, 200, 15))
        self.categorie_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.categorie_erreur.hide()
        
        self.description_erreur = QtWidgets.QLabel(parent=self.frame)
        self.description_erreur.setGeometry(QtCore.QRect(20, 348, 300, 15))
        self.description_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.description_erreur.hide()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Connexion des boutons
        self.boutton_valider.clicked.connect(self.handle_add_product)
        self.boutton_retour.clicked.connect(self.handle_retour)
        self.boutton_quitter.clicked.connect(self.handle_quit)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.titre_ecrit.setText(_translate("Dialog", "Création d\'un produit "))
        self.nom.setText(_translate("Dialog", "Entrer le nom du produit : "))
        self.prix.setText(_translate("Dialog", "Entrer le prix du produit"))
        self.categorie.setText(_translate("Dialog", "Entrer le nom de catégorie du produit"))
        self.boutton_retour.setText(_translate("Dialog", "Retour"))
        self.boutton_quitter.setText(_translate("Dialog", "Quitter"))
        self.description.setText(_translate("Dialog", "Entrer la description du produit : "))
        self.boutton_valider.setText(_translate("Dialog", "Valider"))

    def handle_add_product(self):
        self.logger.info("Tentative d'ajout d'un produit")

        try:
            nom = self.champs_nom.text().capitalize()
            if nom == "":
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_nom.setStyleSheet(error_style)
                
                self.nom_erreur.setText("Le nom du produit ne peut être vide")
                self.nom_erreur.show()
                self.logger.info("Échec : Nom du produit vide")
                return
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.Dialog, "Erreur inattendue", str(e))
            self.logger.exception(f"{str(e)}")
            return
        
        try:
            try:
                prix = float(self.champs_prix.text())
            except ValueError as ve:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_prix.setStyleSheet(error_style)
                
                self.prix_erreur.setText("Vous devez saisir un nombre.")
                self.prix_erreur.show()
                self.logger.info("Échec : Prix du produit pas sous la forme d'un nombre")
                return
            if prix < 0:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_prix.setStyleSheet(error_style)
                
                self.prix_erreur.setText("Le prix du produit ne peut être inférieur à 0")
                self.prix_erreur.show()
                self.logger.info("Échec : Prix du produit inférieur à 0")
                return
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.Dialog, "Erreur inattendue", str(e))
            self.logger.exception(f"{str(e)}")
            return
        
        try:
            categorie = self.champs_categorie.text()
            if categorie == "":
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_categorie.setStyleSheet(error_style)
                
                self.categorie_erreur.setText("Le catégorie du produit ne peut être vide")
                self.categorie_erreur.show()
                self.logger.info("Échec : Catégorie du produit vide")
                return
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.Dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")
            return
        
        try:
            description = self.champs_description.text()

            # Utiliser le chemin correct pour la base de données
            db_path = os.path.join(os.path.dirname(__file__), 'database.db')
            connection = sqlite3.connect(db_path)
            curseur = connection.cursor()
            curseur.execute("INSERT INTO catalogue (nom, prix, categorie, description) VALUES (?, ?, ?, ?)", 
                        (nom, prix, categorie, description))
            connection.commit()

            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText("Le produit a été ajouté avec succès !")
            msg_box.exec()
            self.logger.info(f"Produit ajouté à la base de données.\nNom : {nom}\nPrix : {prix}\nCatégorie : {categorie}\nDescription : {description}")
        
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.warning(self.Dialog, "Erreur de base de données", str(e))
            self.logger.warning(f"{str(e)}")
            return
        
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.Dialog, "Erreur inattendue", str(e))
            self.logger.exception(f"{str(e)}")
            return
        finally:
            if 'connection' in locals():
                connection.close()
        
        try:
            self.logger.info("Retour au menu principal (choisir_action.py) depuis la création du produit (create_product.py)")
            from choisir_action import Ui_Main_Menu
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Main_Menu()
            self.ui.setupUi(self.window, self.username, self.status)
            self.Dialog.close()
            self.window.show()

        except Exception as e:
            QtWidgets.QMessageBox.warning(self.Dialog, "Erreur inattendue", str(e))
            self.logger.exception(f"{str(e)}")

    def handle_retour(self):
        try:
            self.logger.info("Retour au menu principal (choisir_action.py) depuis la création du produit (create_product.py)")
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
    try:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_CreateProduct()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec())

    except Exception as e:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger.exception(f"{str(e)}")