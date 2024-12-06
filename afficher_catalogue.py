from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import os
import logging

class Ui_Catalogue(object):
    def setupUi(self, Dialog, username=None, status=None):
        self.Dialog = Dialog
        self.username = username
        self.status = status
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG, format='[%(asctime)s] %(levelname)s — %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        Dialog.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            #productCard {
                background-color: white;
                border-radius: 8px;
                padding: 16px;
                margin: 8px;
                border: 1px solid #ddd;
            }
            #productCard:hover {
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            #productTitle {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
            }
            #productPrice {
                font-size: 16px;
                color: #27ae60;
                font-weight: bold;
            }
            #productCategory {
                font-size: 14px;
                color: #7f8c8d;
            }
            #productDescription {
                font-size: 14px;
                color: #34495e;
            }
        """)

        # Layout principal
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        
        # En-tête
        self.header = QtWidgets.QHBoxLayout()
        
        # Titre
        self.title = QtWidgets.QLabel("Catalogue des Produits")
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 20px;
        """)
        self.header.addWidget(self.title)
        
        # Barre de recherche
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un produit...")
        self.search_input.setMinimumWidth(300)
        self.search_button = QtWidgets.QPushButton("Rechercher")
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.header.addLayout(self.search_layout)
        
        # Filtres et tri
        self.filter_layout = QtWidgets.QHBoxLayout()
        
        # Filtre par catégorie
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItem("Toutes les catégories")
        self.filter_layout.addWidget(QtWidgets.QLabel("Catégorie:"))
        self.filter_layout.addWidget(self.category_combo)
        
        # Options de tri
        self.sort_combo = QtWidgets.QComboBox()
        self.sort_combo.addItems([
            "Trier par...",
            "Prix croissant",
            "Prix décroissant",
            "Nom A-Z",
            "Nom Z-A",
            "Catégorie"
        ])
        self.filter_layout.addWidget(QtWidgets.QLabel("Trier par:"))
        self.filter_layout.addWidget(self.sort_combo)
        
        self.header.addLayout(self.filter_layout)
        self.main_layout.addLayout(self.header)
        
        # Zone de défilement pour les produits
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_content)
        
        # Chargement des produits
        self.load_products()
        
        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        
        # Bouton Retour
        self.button_layout = QtWidgets.QHBoxLayout()
        self.retour_button = QtWidgets.QPushButton("Retour")
        self.button_layout.addWidget(self.retour_button)
        self.main_layout.addLayout(self.button_layout)
        
        # Connexions
        self.retour_button.clicked.connect(self.handle_retour)
        self.search_button.clicked.connect(self.search_products)
        self.search_input.returnPressed.connect(self.search_products)
        self.category_combo.currentTextChanged.connect(self.filter_by_category)
        self.sort_combo.currentTextChanged.connect(self.sort_products)
        
        self.load_categories()

    def create_product_card(self, product):
        """Crée une carte pour afficher un produit"""
        card = QtWidgets.QWidget()
        card.setObjectName("productCard")
        card.setMinimumWidth(350)
        card.setMaximumWidth(350)
        
        layout = QtWidgets.QVBoxLayout(card)
        
        # ID du produit
        id_label = QtWidgets.QLabel(f"ID: {product[0]}")
        id_label.setObjectName("productId")
        id_label.setStyleSheet("""
            color: #666666;
            font-size: 12px;
            font-style: italic;
        """)
        layout.addWidget(id_label)
        
        # Titre du produit
        title = QtWidgets.QLabel(product[1])  # nom
        title.setObjectName("productTitle")
        layout.addWidget(title)
        
        # Prix
        price = QtWidgets.QLabel(f"{product[2]:.2f} €")  # prix
        price.setObjectName("productPrice")
        layout.addWidget(price)
        
        # Catégorie
        category = QtWidgets.QLabel(product[3])  # categorie
        category.setObjectName("productCategory")
        layout.addWidget(category)
        
        # Description
        description = QtWidgets.QLabel(product[4])  # description
        description.setObjectName("productDescription")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        return card

    def load_products(self, search_term=None, category=None, sort_option=None):
        """Charge les produits depuis la base de données"""
        try:
            # Nettoyer la grille existante
            for i in reversed(range(self.grid_layout.count())): 
                self.grid_layout.itemAt(i).widget().setParent(None)
            
            connection = sqlite3.connect("projet_python/database.db")
            cursor = connection.cursor()
            
            query = "SELECT * FROM catalogue"
            params = []
            
            # Construction de la clause WHERE
            where_clauses = []
            if search_term:
                where_clauses.append("(nom LIKE ? OR description LIKE ?)")
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            if category and category != "Toutes les catégories":
                where_clauses.append("categorie = ?")
                params.append(category)
            
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            
            # Ajout du tri
            if sort_option:
                if sort_option == "Prix croissant":
                    query += " ORDER BY prix ASC"
                elif sort_option == "Prix décroissant":
                    query += " ORDER BY prix DESC"
                elif sort_option == "Nom A-Z":
                    query += " ORDER BY nom ASC"
                elif sort_option == "Nom Z-A":
                    query += " ORDER BY nom DESC"
                elif sort_option == "Catégorie":
                    query += " ORDER BY categorie ASC, nom ASC"
            
            cursor.execute(query, params)
            products = cursor.fetchall()
            
            # Affichage des produits dans une grille
            row = 0
            col = 0
            for product in products:
                card = self.create_product_card(product)
                self.grid_layout.addWidget(card, row, col)
                col += 1
                if col > 2:  # 3 produits par ligne
                    col = 0
                    row += 1
            
            # Ajouter un widget extensible à la fin
            spacer = QtWidgets.QWidget()
            spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, 
                               QtWidgets.QSizePolicy.Policy.Expanding)
            self.grid_layout.addWidget(spacer, row + 1, 0)
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des produits : {str(e)}")
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Erreur",
                "Une erreur est survenue lors du chargement des produits."
            )
        finally:
            if 'connection' in locals():
                connection.close()

    def load_categories(self):
        """Charge les catégories depuis la base de données"""
        try:
            connection = sqlite3.connect("projet_python/database.db")
            cursor = connection.cursor()
            
            cursor.execute("SELECT DISTINCT categorie FROM catalogue")
            categories = cursor.fetchall()
            
            for category in categories:
                self.category_combo.addItem(category[0])
                
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des catégories : {str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()

    def search_products(self):
        """Recherche des produits"""
        search_term = self.search_input.text()
        category = self.category_combo.currentText()
        sort_option = self.sort_combo.currentText()
        if sort_option == "Trier par...":
            sort_option = None
        self.load_products(search_term, category, sort_option)

    def filter_by_category(self, category):
        """Filtre les produits par catégorie"""
        search_term = self.search_input.text()
        sort_option = self.sort_combo.currentText()
        if sort_option == "Trier par...":
            sort_option = None
        self.load_products(search_term, category, sort_option)

    def sort_products(self, sort_option):
        """Trie les produits"""
        if sort_option == "Trier par...":
            sort_option = None
        search_term = self.search_input.text()
        category = self.category_combo.currentText()
        self.load_products(search_term, category, sort_option)

    def handle_retour(self):
        try:
            self.logger.info("Retour au menu principal (choisir_action.py) depuis le catalogue (afficher_catalogue.py)")
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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Catalogue()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec()) 