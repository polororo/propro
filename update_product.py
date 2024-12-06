from PyQt6 import QtCore, QtGui, QtWidgets
import logging
import sqlite3

class Ui_UpdateProduct(object):
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

        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(-14, -8, 701, 521))
        self.label.setPixmap(QtGui.QPixmap("./new/Pictures/fond.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.champs_id = QtWidgets.QLineEdit(parent=self.frame)
        self.champs_id.setGeometry(QtCore.QRect(170, 80, 200, 30))
        self.champs_id.setObjectName("champs_id")

        self.label_id = QtWidgets.QLabel(parent=self.frame)
        self.label_id.setGeometry(QtCore.QRect(170, 50, 200, 20))
        self.label_id.setStyleSheet("color: rgb(255, 255, 255);")

        self.boutton_rechercher = QtWidgets.QPushButton(parent=self.frame)
        self.boutton_rechercher.setGeometry(QtCore.QRect(390, 80, 100, 30))

        self.nom = QtWidgets.QLabel(parent=self.frame)
        self.nom.setGeometry(QtCore.QRect(170, 130, 200, 20))
        self.nom.setStyleSheet("color: rgb(255, 255, 255);")

        self.champs_nom = QtWidgets.QLineEdit(parent=self.frame)
        self.champs_nom.setGeometry(QtCore.QRect(170, 160, 200, 30))
        self.champs_nom.setObjectName("champs_nom")

        self.prix = QtWidgets.QLabel(parent=self.frame)
        self.prix.setGeometry(QtCore.QRect(170, 200, 200, 20))
        self.prix.setStyleSheet("color: rgb(255, 255, 255);")

        self.champs_prix = QtWidgets.QLineEdit(parent=self.frame)
        self.champs_prix.setGeometry(QtCore.QRect(170, 230, 200, 30))
        self.champs_prix.setObjectName("champs_prix")

        self.categorie = QtWidgets.QLabel(parent=self.frame)
        self.categorie.setGeometry(QtCore.QRect(170, 270, 200, 20))
        self.categorie.setStyleSheet("color: rgb(255, 255, 255);")

        self.champs_categorie = QtWidgets.QLineEdit(parent=self.frame)
        self.champs_categorie.setGeometry(QtCore.QRect(170, 300, 200, 30))
        self.champs_categorie.setObjectName("champs_categorie")

        self.description = QtWidgets.QLabel(parent=self.frame)
        self.description.setGeometry(QtCore.QRect(170, 340, 200, 20))
        self.description.setStyleSheet("color: rgb(255, 255, 255);")

        self.champs_description = QtWidgets.QLineEdit(parent=self.frame)
        self.champs_description.setGeometry(QtCore.QRect(170, 370, 200, 30))
        self.champs_description.setObjectName("champs_description")

        self.boutton_valider = QtWidgets.QPushButton(parent=self.frame)
        self.boutton_valider.setGeometry(QtCore.QRect(390, 370, 100, 30))

        self.retour_quitter = QtWidgets.QFrame(parent=self.frame)
        self.retour_quitter.setGeometry(QtCore.QRect(60, 400, 550, 80))
        self.retour_quitter.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.retour_quitter.setObjectName("retour_quitter")

        self.boutton_retour = QtWidgets.QPushButton(parent=self.retour_quitter)
        self.boutton_retour.setGeometry(QtCore.QRect(0, 40, 111, 41))
        self.boutton_retour.setObjectName("boutton_retour")
        
        self.boutton_quitter = QtWidgets.QPushButton(parent=self.retour_quitter)
        self.boutton_quitter.setGeometry(QtCore.QRect(400, 40, 111, 41))
        self.boutton_quitter.setObjectName("boutton_quitter")

        # Définition des labels d'erreur
        self.id_erreur = QtWidgets.QLabel(parent=self.frame)
        self.id_erreur.setGeometry(QtCore.QRect(170, 108, 200, 15))
        self.id_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.id_erreur.hide()

        self.nom_erreur = QtWidgets.QLabel(parent=self.frame)
        self.nom_erreur.setGeometry(QtCore.QRect(170, 188, 200, 15))
        self.nom_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.nom_erreur.hide()

        self.prix_erreur = QtWidgets.QLabel(parent=self.frame)
        self.prix_erreur.setGeometry(QtCore.QRect(170, 258, 200, 15))
        self.prix_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.prix_erreur.hide()

        self.categorie_erreur = QtWidgets.QLabel(parent=self.frame)
        self.categorie_erreur.setGeometry(QtCore.QRect(170, 328, 200, 15))
        self.categorie_erreur.setStyleSheet("color: red; font-size: 10px;")
        self.categorie_erreur.hide()

        # Connexion des boutons
        self.boutton_rechercher.clicked.connect(self.handle_search)
        self.boutton_valider.clicked.connect(self.handle_update)
        self.boutton_retour.clicked.connect(self.handle_retour)
        self.boutton_quitter.clicked.connect(self.handle_quit)

        #
        self.product_id = -1

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Modifier un produit"))
        self.titre_ecrit.setText(_translate("Dialog", "Modifier un produit"))
        self.label_id.setText(_translate("Dialog", "Entrez un identifiant produit :"))
        self.boutton_rechercher.setText(_translate("Dialog", "Rechercher"))
        self.nom.setText(_translate("Dialog", "Nom :"))
        self.prix.setText(_translate("Dialog", "Prix :"))
        self.categorie.setText(_translate("Dialog", "Categorie :"))
        self.description.setText(_translate("Dialog", "Description :"))
        self.boutton_valider.setText(_translate("Dialog", "Modifier"))
        self.boutton_retour.setText(_translate("Dialog", "Retour"))
        self.boutton_quitter.setText(_translate("Dialog", "Quitter"))

    def handle_search(self):
        self.logger.info("Tentative de modification d'un produit : recherche de l'ID")
        try:
            self.product_id = self.champs_id.text()
            self.logger.info(f"Recherche avec ID : {self.product_id}")
            if not self.verif_id():
                return

            connection = sqlite3.connect("projet_python/database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM catalogue WHERE id = ?", (self.product_id,))
            result = cursor.fetchone()
            self.champs_nom.setText(result[1])
            self.champs_prix.setText(str(result[2]))
            self.champs_categorie.setText(result[3])
            self.champs_description.setText(result[4])
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

    def handle_update(self):
        self.logger.info("Tentative de modification d'un produit : modification des champs")

        try:
            if not self.verif_id():
                return
            
            try:
                name = self.champs_nom.text().capitalize()
                if name == "":
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
                    price = float(self.champs_prix.text())
                except ValueError as ve:
                    error_style = "border: 1px solid red; border-radius: 3px;"
                    self.champs_prix.setStyleSheet(error_style)
                    
                    self.prix_erreur.setText("Vous devez saisir un nombre.")
                    self.prix_erreur.show()
                    self.logger.info("Échec : Prix du produit pas sous la forme d'un nombre")
                    return
                if price < 0:
                    error_style = "border: 1px solid red; border-radius: 3px;"
                    self.champs_prix.setStyleSheet(error_style)
                    
                    self.prix_erreur.setText("Le prix du produit ne peut être inférieur à 0")
                    self.prix_erreur.show()
                    self.logger.info("Échec : Prix du produit inférieur à 0")
                    return
                
            except Exception as e:
                QtWidgets.QMessageBox.warning(Dialog, "Erreur inattendue", str(e))
                self.logger.exception(f"{str(e)}")
                return
            
            try:
                category = self.champs_categorie.text()
                if category == "":
                    error_style = "border: 1px solid red; border-radius: 3px;"
                    self.champs_categorie.setStyleSheet(error_style)
                    
                    self.categorie_erreur.setText("Le catégorie du produit ne peut être vide")
                    self.categorie_erreur.show()
                    self.logger.info("Échec : Catégorie du produit vide")
                    return
                
            except Exception as e:
                QtWidgets.QMessageBox.warning(Dialog, "Erreur inattendue", str(e))
                self.logger.exception(f"{str(e)}")
                return
        
            description = self.champs_description.text()

            connection = sqlite3.connect("projet_python/database.db")
            cursor = connection.cursor()
            cursor.execute("UPDATE catalogue SET nom = ?, prix = ?, categorie = ?, description = ? WHERE id = ?",
                           (name, price, category, description, self.product_id))
            connection.commit()

            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText("Le produit a été modifié avec succés !")
            msg_box.exec()

            self.logger.info(f"Le produit ayant pour ID : '{self.product_id}' a été modifié")

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.warning(Dialog, "Erreur de base de données", str(e))
            self.logger.warning(f"{str(e)}")
            return
        
        except Exception as e:
            QtWidgets.QMessageBox.warning(Dialog, "Erreur inattendue", str(e) )
            self.logger.exception(f"{str(e)}")
            return
        finally:
            if 'connection' in locals():
                connection.close()
        
        try:
            self.logger.info("Retour au menu principal (choisir_action.py) depuis la modification de produit (update_product.py)")
            from choisir_action import Ui_Main_Menu
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Main_Menu()
            self.ui.setupUi(self.window, self.username, self.status)
            Dialog.close()
            self.window.show()

        except Exception as e:
            QtWidgets.QMessageBox.warning(Dialog, "Erreur inattendue", str(e))
            self.logger.exception(f"{str(e)}")

    def verif_id(self):
        try:
            if self.product_id == "":
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_id.setStyleSheet(error_style)
                
                self.id_erreur.setText("Le champ ne peut être vide")
                self.id_erreur.show()
                self.logger.info("Échec : Champ vide")
                return False
            
            try:
                self.product_id = float(self.product_id)
            except ValueError as ve:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_id.setStyleSheet(error_style)
                
                self.id_erreur.setText("Vous devez saisir un nombre.")
                self.id_erreur.show()
                self.logger.info("Échec : Prix du produit pas sous la forme d'un nombre")
                return False
            
            connection = sqlite3.connect("projet_python/database.db")
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM catalogue WHERE id = ?", (self.product_id,))
            if cursor.fetchone()[0] <= 0:
                error_style = "border: 1px solid red; border-radius: 3px;"
                self.champs_id.setStyleSheet(error_style)
                
                self.id_erreur.setText("Identifiant invalide")
                self.id_erreur.show()
                self.logger.info("Échec : Identifiant invalide")
                return False
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.warning(Dialog, "Erreur de base de données", str(e))
            self.logger.warning(f"{str(e)}")
            return False
        
        except Exception as e:
            QtWidgets.QMessageBox.warning(Dialog, "Erreur inattendue", str(e) )
            self.logger.exception(f"{str(e)}")
            return False
        finally:
            if 'connection' in locals():
                connection.close()
        return True
            

    def handle_retour(self):
        try:
            self.logger.info("Retour au menu principal (choisir_action.py) depuis la modification de produit (update_product.py)")
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
        ui = Ui_UpdateProduct()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec())

    except Exception as e:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger.exception(f"{str(e)}")