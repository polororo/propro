from PyQt6 import QtCore, QtGui, QtWidgets
import pyotp
import qrcode
from io import BytesIO
import sqlite3
import logging

class QRCode2FA(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setupUi(self, Dialog, username):
        self.dialog = Dialog
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(400, 500)
        
        # Configuration du layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        
        # Label pour le titre
        self.title_label = QtWidgets.QLabel(Dialog)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setText("Configuration de l'authentification à deux facteurs")
        self.verticalLayout.addWidget(self.title_label)
        
        # Label pour le QR Code
        self.qr_label = QtWidgets.QLabel(Dialog)
        self.qr_label.setMinimumSize(QtCore.QSize(300, 300))
        self.qr_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.qr_label)
        
        # Label pour les instructions
        self.instructions_label = QtWidgets.QLabel(Dialog)
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setText("1. Scannez ce QR code avec votre application d'authentification (Google Authenticator, Authy, etc.)\n2. Une fois scanné, cliquez sur Continuer")
        self.verticalLayout.addWidget(self.instructions_label)
        
        # Bouton Continuer
        self.continue_button = QtWidgets.QPushButton(Dialog)
        self.continue_button.setText("Continuer")
        self.continue_button.clicked.connect(lambda: self.redirect_to_login(username))
        self.verticalLayout.addWidget(self.continue_button)
        
        # Générer et afficher le QR code
        self.generate_and_show_qr(username)

    def generate_and_show_qr(self, username):
        try:
            # Générer une clé secrète pour TOTP
            secret = pyotp.random_base32()
            
            # Créer l'URI TOTP
            totp = pyotp.TOTP(secret)
            provisioning_uri = totp.provisioning_uri(username, issuer_name="CatalogueApp")
            
            # Générer le QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            # Convertir le QR code en image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir l'image en QPixmap pour l'affichage
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_image = QtGui.QImage.fromData(buffer.getvalue())
            qr_pixmap = QtGui.QPixmap.fromImage(qr_image)
            
            # Redimensionner le QR code
            scaled_pixmap = qr_pixmap.scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            self.qr_label.setPixmap(scaled_pixmap)
            
            # Sauvegarder la clé secrète dans la base de données
            self.save_secret_to_db(username, secret)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du QR code: {str(e)}")
            QtWidgets.QMessageBox.critical(self.dialog, "Erreur", "Erreur lors de la génération du QR code")

    def save_secret_to_db(self, username, secret):
        try:
            connection = sqlite3.connect("projet_python/database.db")
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET otp_secret = ? WHERE username = ?", (secret, username))
            connection.commit()
            connection.close()
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la clé secrète: {str(e)}")
            raise

    def redirect_to_login(self, username):
        try:
            self.logger.info(f"Redirection vers la page de connexion pour l'utilisateur {username}")
            from login import Ui_Login
            self.window = QtWidgets.QDialog()
            self.ui = Ui_Login()
            self.ui.setupUi(self.window)
            self.dialog.close()
            self.window.show()
        except Exception as e:
            self.logger.error(f"Erreur lors de la redirection: {str(e)}")
            QtWidgets.QMessageBox.critical(self.dialog, "Erreur", "Erreur lors de la redirection") 