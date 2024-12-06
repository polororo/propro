from PyQt6 import QtCore, QtGui, QtWidgets
import logging

class Ui_question(object):
    def setupUi(self, Dialog, message):
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

        
        # Définition des labels d'erreur
        self.question_label = QtWidgets.QLabel(parent=self.dialog)
        self.question_label.setGeometry(QtCore.QRect(75, 118, 520, 41))
        self.question_label.setStyleSheet("color: white; font-size: 20px;")
        self.question_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.question_label.setObjectName("question_label")
        
        # Définition du bouton de validation
        self.yes_button = QtWidgets.QPushButton(parent=self.dialog)
        self.yes_button.setGeometry(QtCore.QRect(210, 250, 111, 41))
        self.yes_button.setObjectName("yes_button")
        
        # Définition du bouton de validation
        self.no_button = QtWidgets.QPushButton(parent=self.dialog)
        self.no_button.setGeometry(QtCore.QRect(350, 250, 111, 41))
        self.no_button.setObjectName("no_button")

        self.retranslateUi(message)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

        # Connexion des boutons
        self.yes_button.clicked.connect(self.handle_yes)
        self.no_button.clicked.connect(self.handle_no)

    def retranslateUi(self, message):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Connexion"))
        self.question_label.setText(_translate("Dialog", message))
        self.yes_button.setText(_translate("Dialog", " Oui"))
        self.no_button.setText(_translate("Dialog", " Non"))

    def handle_yes(self):
        self.result = True  # Définit le résultat lorsque le bouton "Oui" est cliqué
        self.dialog.accept()  # Ferme la boîte de dialogue

    def handle_no(self):
        self.result = False  # Définit le résultat lorsque le bouton "Non" est cliqué
        self.dialog.accept()  # Ferme la boîte de dialogue

    def get_result(self):
        return self.result  # Renvoie le résultat


if __name__ == "__main__":
    try:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_question()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec())

    except Exception as e:
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger.exception(f"(5) : {str(e)}")