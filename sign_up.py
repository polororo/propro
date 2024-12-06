from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import hashlib
import logging

class Sign_Up(object):
    def setupUi(self, Dialog):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        self.dialog = Dialog
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(670, 500)
        self.dialog.setMinimumSize(QtCore.QSize(670, 500))
        self.dialog.setMaximumSize(QtCore.QSize(670, 500))

        # Définition du background
        self.label = QtWidgets.QLabel(parent=self.dialog)
        self.label.setGeometry(QtCore.QRect(-130, -50, 831, 581))
        self.label.setPixmap(QtGui.QPixmap("./new/Pictures/fond.png"))
        self.label.setObjectName("background")

        # Définition de l'entrée texte pour le nom d'utilisateur
        self.username_input = QtWidgets.QLineEdit(parent=self.dialog)
        self.username_input.setGeometry(QtCore.QRect(250, 90, 171, 30))
        self.username_input.setText("")
        self.username_input.setObjectName("username_input")

        # Définition de l'entrée texte pour le mot de passe
        self.password_input = QtWidgets.QLineEdit(parent=self.dialog)
        self.password_input.setGeometry(QtCore.QRect(250, 140, 171, 30))
        self.password_input.setText("")
        self.password_input.setObjectName("lineEdit")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        # Définition de l'entrée texte pour la confirmation de mot de passe
        self.password_confirmation_input = QtWidgets.QLineEdit(parent=self.dialog)
        self.password_confirmation_input.setGeometry(QtCore.QRect(250, 190, 171, 30))
        self.password_confirmation_input.setText("")
        self.password_confirmation_input.setObjectName("password_confirmation_input")
        self.password_confirmation_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        # Définition du bouton de validation
        self.signup_button = QtWidgets.QPushButton(parent=self.dialog)
        self.signup_button.setGeometry(QtCore.QRect(280, 240, 111, 41))
        self.signup_button.setObjectName("signup_button")

        # Définition du bouton redirigeant vers le menu de connexion
        self.retour_button = QtWidgets.QPushButton(parent=self.dialog)
        self.retour_button.setGeometry(QtCore.QRect(200, 310, 111, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./new/Pictures/icone 2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.retour_button.setIcon(icon)
        self.retour_button.setObjectName("retour_button")

        # Définition du bouton arrêtant le programme
        self.quit_button = QtWidgets.QPushButton(parent=self.dialog)
        self.quit_button.setGeometry(QtCore.QRect(360, 310, 111, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./new/Pictures/icone.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.quit_button.setIcon(icon1)
        self.quit_button.setObjectName("quit_button")

        # Connexion des boutons
        self.signup_button.clicked.connect(self.add_user)
        self.retour_button.clicked.connect(self.handle_retour)
        self.quit_button.clicked.connect(self.handle_quit)

        # Définition des labels d'erreur
        self.username_error = QtWidgets.QLabel(parent=self.dialog)
        self.username_error.setGeometry(QtCore.QRect(250, 118, 171, 15))
        self.username_error.setStyleSheet("color: red; font-size: 10px;")
        self.username_error.hide()

        self.password_error = QtWidgets.QLabel(parent=self.dialog)
        self.password_error.setGeometry(QtCore.QRect(250, 168, 171, 15))
        self.password_error.setStyleSheet("color: red; font-size: 10px;")
        self.password_error.hide()
        
        self.password_confirmation_error = QtWidgets.QLabel(parent=self.dialog)
        self.password_confirmation_error.setGeometry(QtCore.QRect(250, 218, 171, 15))
        self.password_confirmation_error.setStyleSheet("color: red; font-size: 10px;")
        self.password_confirmation_error.hide()

        self.retranslateUi(self.dialog)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Création de compte"))
        self.signup_button.setText(_translate("Dialog", "Valider"))
        self.username_input.setPlaceholderText(_translate("Dialog", "Entrez votre identifiant"))
        self.password_input.setPlaceholderText(_translate("Dialog", "Entrez votre mot de passe"))
        self.password_confirmation_input.setPlaceholderText(_translate("Dialog", "Confirmez votre mot de passe"))
        self.retour_button.setText(_translate("Dialog", " Retour"))
        self.quit_button.setText(_translate("Dialog", " Quitter"))
            
    def add_user(self):
        self.logger.info(f"Tentative de création de compte")
        try:
            connection = sqlite3.connect("projet_python/database.db")
            curseur = connection.cursor()

            sign_up_state = False
            while (sign_up_state != True):
                try:
                    username = self.username_input.text()
                    if username == "":
                        error_style = "border: 1px solid red; border-radius: 3px;"
                        self.username_input.setStyleSheet(error_style)
                        
                        self.username_error.setText("Le nom d'utilisateur ne peut être vide")
                        self.username_error.show()
                        self.logger.info("Échec : Nom d'utilisateur vide")
                        return
                    curseur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
                    if curseur.fetchone()[0] > 0:
                        error_style = "border: 1px solid red; border-radius: 3px;"
                        self.username_input.setStyleSheet(error_style)
                        
                        self.username_error.setText("Ce nom d'utilisateur existe déjà.")
                        self.username_error.show()
                        self.logger.info("Échec : Nom d'utilisateur déjà pris")
                        return
                    
                except Exception as e:
                    
                    QtWidgets.QMessageBox.warning(
                            self.dialog,
                            "Erreur inattendue",
                            str(e)
                        )
                    self.logger.exception(f"{str(e)}")
                    return
                
                # Vérification de la robusté du mot de passe
                password = self.password_input.text()
                try:
                    from password_verification import password_verification
                    valid = password_verification(password)
                    if not valid[0]:
                        # Affichage des messages d'erreur en dessous des entrées texte
                        error_style = "border: 1px solid red; border-radius: 3px;"
                        self.password_input.setStyleSheet(error_style)
                        self.password_confirmation_input.setStyleSheet(error_style)
                        
                        self.password_error.setText("Min. 8 caractères, 1 minuscule, 1 majuscule, 1 chiffre")
                        self.password_confirmation_error.setText("Min. 8 caractères, 1 minuscule, 1 majuscule, 1 chiffre")
                        self.password_error.show()
                        self.password_confirmation_error.show()
                        self.logger.info(f"Échec : Le mot de passe ne respecte pas les conditions ({valid[1]})")

                        # Création d'une fenêtre pop-up avec un message d'erreur
                        msg_box = QtWidgets.QMessageBox()
                        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        msg_box.setWindowTitle("Erreur")
                        msg_box.setText("Votre mot de passe doit être composé de minimum 8 caractères donc au moins 1 minuscule, 1 majuscule et 1 chiffre.")
                        msg_box.exec()
                        return
                    
                except Exception as e:
                    
                    QtWidgets.QMessageBox.warning(
                            self.dialog,
                            "Erreur inattendue",
                            str(e)
                        )
                    self.logger.exception(f"{str(e)}")
                    return

                try:
                    # Vérification de la compromission du mot de passe
                    from password_verification import hibp_verification
                    compromise = hibp_verification(password)
                    if compromise[0]:
                        self.logger.info(f"Le mot de passe a déjà été compromis")

                        # Affichage de la page demandant à l'utilisateur s'il veut générer un mot de passe
                        from ask_question import Ui_question
                        Dialog = QtWidgets.QDialog()
                        ui = Ui_question()
                        ui.setupUi(Dialog, "Voulez-vous générer un mot de passe automatiquement ?")
                        Dialog.exec() # Vérifie si la boîte de dialogue a été acceptée
                        result = ui.get_result()  # Obtient le résultat
                        
                        # Génération du mot de passe si choix positif de l'utilisateur
                        if result:
                            self.logger.info(f"Génération d'un mot de passe robuste")
                            from password_verification import generate_password
                            password = generate_password()

                            # Création d'une fenêtre pop-up pour afficher le mot de passe à l'utilisateur
                            msg_box = QtWidgets.QMessageBox()
                            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
                            msg_box.setWindowTitle("Mot de passe")
                            password_display = QtWidgets.QLineEdit()
                            password_display.setText(password)
                            password_display.setReadOnly(True)
                            password_display.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
                            msg_box.layout().addWidget(password_display)
                            msg_box.setText(f"Voici le mot de passe généré : {password} \nPensez à le mémoriser, mais attention à ne pas le noter de façon non sécurisée !")
                            msg_box.exec()
                        return
                    
                except Exception as e:
                    
                    QtWidgets.QMessageBox.warning(
                            self.dialog,
                            "Erreur inattendue",
                            str(e)
                        )
                    self.logger.exception(f"{str(e)}")
                    return

                try:
                    # Vérification si les mots de passe correspondent
                    password = hashlib.sha256(password.encode('UTF-8')).hexdigest().upper()
                    conf = hashlib.sha256(self.password_confirmation_input.text().encode('UTF-8')).hexdigest().upper()
                    if password != conf:
                        # Affichage des messages d'erreur en dessous des entrées texte
                        error_style = "border: 1px solid red; border-radius: 3px;"
                        self.password_input.setStyleSheet(error_style)
                        self.password_confirmation_input.setStyleSheet(error_style)
                        
                        self.password_error.setText("Identifiants incorrects")
                        self.password_confirmation_error.setText("Identifiants incorrects")
                        self.password_error.show()
                        self.password_confirmation_error.show()
                        self.logger.info("Échec : Les mots de passe ne correspondent pas")

                        # Création d'une fenêtre pop-up avec un message d'erreur
                        msg_box = QtWidgets.QMessageBox()
                        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        msg_box.setWindowTitle("Erreur")
                        msg_box.setText("Les mots de passe ne correspondent pas.")
                        msg_box.exec()

                        # Réinitialiser l'état du formulaire pour permettre à l'utilisateur de saisir à nouveau
                        self.password_input.clear()
                        self.password_confirmation_input.clear()
                        return  # On arrête le processus et attend une nouvelle saisie
                    
                except Exception as e:
                    
                    QtWidgets.QMessageBox.warning(
                            self.dialog,
                            "Erreur inattendue",
                            str(e)
                        )
                    self.logger.exception(f"{str(e)}")
                    return
            
                sign_up_state = True
            valid_statuses = {"admin", "editor", "user"}
            while True:
                status = "user"
                if status not in valid_statuses:
                    print(f"Statut invalide. Choisissez parmi {', '.join(valid_statuses)}.")
                else:
                    break

            curseur.execute("INSERT INTO users (username, password, status) VALUES (?, ?, ?)", (username, password, status))
            connection.commit()

            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText("L'utilisateur a été ajouté avec succés !")
            msg_box.exec()
            self.logger.info(f"L'utilisateur '{username}' a été ajouté à la base de donnée")
            self.open_login_page()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.warning(
                    self.dialog,
                    "Erreur de base de données",
                    str(e)
                )
            self.logger.warning(f"{str(e)}")
        except Exception as e:
            
            QtWidgets.QMessageBox.warning(
                    self.dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()
            
    def open_login_page(self):
        try:
            self.logger.info("Affichage de la page de configuration 2FA")
            from genere_qrcode_2FA import QRCode2FA
            self.window = QtWidgets.QDialog()
            qr_ui = QRCode2FA()
            qr_ui.setupUi(self.window, self.username_input.text())
            self.dialog.close()
            self.window.show()

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.dialog,
                    "Erreur inattendue",
                    str(e)
                )
            self.logger.exception(f"{str(e)}")

    def handle_retour(self):
        try:
            self.logger.info("Retour au menu principal (menu.py) depuis la page de connexion (login.py)")
            from menu import Ui_Menu
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Menu()
            self.ui.setupUi(self.window)
            self.dialog.close()
            self.window.show()

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                    self.dialog,
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
        ui = Sign_Up()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec())

    except Exception as e:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger.exception(f"{str(e)}")