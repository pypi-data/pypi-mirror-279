import os
import sys
import json
from pathlib import Path
from threading import Thread
import subprocess
import requests
import psycopg2
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QWidget, QLabel, QComboBox, QInputDialog
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import QTranslator

class CrlBrowserHTTPRequestHandler(SimpleHTTPRequestHandler):
    def address_string(self):
        return 'crl-browser'

class ArchBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("crl-browser - Search Engine")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(["English", "Turkish"])  # Supported languages
        self.language_combo_box.currentIndexChanged.connect(self.change_language)
        self.layout.addWidget(self.language_combo_box)

        self.instruction_text_edit = QTextEdit()
        self.instruction_text_edit.setReadOnly(True)
        self.instruction_text_edit.setStyleSheet("background-color: black; color: #00FFFF;")  # Arch Linux colors
        self.instruction_text_edit.setFont(QFont("Courier", 10))
        self.instruction_text_edit.append(self.tr("Welcome! You can search 'crl://' sites from here."))
        self.layout.addWidget(self.instruction_text_edit)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet("background-color: black; color: #00FFFF;")  # Arch Linux colors
        self.search_input.setFont(QFont("Courier", 10))
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: black; color: #00FFFF;")  # Arch Linux colors
        self.search_button.clicked.connect(self.search_sites)
        self.layout.addWidget(self.search_button)

        self.ddns_button = QPushButton("DDNS Manager")  # "DDNS Manager" butonu oluşturuldu
        self.ddns_button.clicked.connect(self.ddns_manager)  # "DDNS Manager" butonunun tıklama işlevi bağlandı
        self.layout.addWidget(self.ddns_button)  # "DDNS Manager" butonu arayüze eklendi

    def ddns_manager(self):
        subprocess.run("ddns.exe")

        # Main crlnet directory
        self.crlnet_directory = str(Path.home())  # Get home directory path

        # Create directory if it doesn't exist
        if not os.path.exists(self.crlnet_directory):
            os.makedirs(self.crlnet_directory)

        # File path to store user info
        self.user_info_file = os.path.join(self.crlnet_directory, "loginusers/users.json")  # Path for user info relative to home directory
        self.load_user_info()

        # Start the web server
        self.server_thread = Thread(target=self.start_server)
        self.server_thread.start()

        # Load logo
        self.load_logo()

        # Translation
        self.translator = QTranslator()

        # PostgreSQL database connection
        self.db_connection = psycopg2.connect(
            dbname="crlnet",
            user="postgres",
            password="goychay_23",
            host="192.168.0.105",
            port="5432"
        )

    def start_server(self):
        try:
            # Get IP address
            ip_address = self.get_ip_address()
            # Start the web server
            self.server = HTTPServer((ip_address, 8000), CrlBrowserHTTPRequestHandler)
            self.instruction_text_edit.append(f"Server started: http://{ip_address}:8080")
            self.server.serve_forever()
        except Exception as e:
            print("Web server could not be started:", e)

    def get_ip_address(self):
        # Get IP address using platform-specific methods
        if sys.platform.startswith('linux') or sys.platform == 'darwin':  # Linux or macOS
            import socket
            return socket.gethostbyname(socket.gethostname())
        elif sys.platform == 'win32':  # Windows
            import socket
            return socket.gethostbyname(socket.gethostname())

    def load_logo(self):
        # Find logo image
        logo_path = os.path.join(self.crlnet_directory, "icon/logo.png")
        if os.path.exists(logo_path):
            self.display_logo(logo_path)
        else:
            self.instruction_text_edit.append("Logo not found. Loading default logo...")
            # Use 'logo.png' as the default logo
            default_logo_path = os.path.join(self.crlnet_directory, "logo.png")
            with open(default_logo_path, "wb") as file:
                response = requests.get("https://example.com/default_logo.png")
                file.write(response.content)
            self.display_logo(default_logo_path)

    def display_logo(self, logo_path):
        # Show the logo image
        pixmap = QPixmap(logo_path)
        self.logo_label = QLabel()
        self.logo_label.setPixmap(pixmap)
        self.layout.addWidget(self.logo_label)

    def search_sites(self):
        search_term = self.search_input.text().strip().lower()
        self.instruction_text_edit.clear()
        self.instruction_text_edit.append(f"Searching for '{search_term}'...")

        # Search domains in the database
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM domains WHERE name ILIKE %s", ('%' + search_term + '%',))
        found_sites = cursor.fetchall()

        if found_sites:
            self.instruction_text_edit.append("Results found:")
            for site in found_sites:
                self.instruction_text_edit.append(site[0])  # Fetch the domain name from the tuple
                # Get and display site content if available
                site_content = self.get_site_content(site[0])
                if site_content:
                    self.display_site_content(site_content)
                else:
                    self.instruction_text_edit.append("No site content available.")
        else:
            self.instruction_text_edit.append("No results found.")

    def get_site_content(self, site_name):
        site_path = os.path.join(self.crlnet_directory, site_name)
        supported_extensions = ['.html', '.php', '.pl', '.txt']
        try:
            for root, _, files in os.walk(site_path):
                for file in files:
                    if any(file.endswith(ext) for ext in supported_extensions):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r") as f:
                            return f.read()
        except Exception as e:
            print(f"Failed to read file: {e}")
        return None

    def display_site_content(self, content):
        self.instruction_text_edit.append("Site Content:")
        self.instruction_text_edit.append(content)

    def save_search_term(self, search_term):
        # Load saved search terms
        search_terms_file = os.path.join(self.crlnet_directory, "search_terms.json")
        if os.path.exists(search_terms_file):
            with open(search_terms_file, "r") as file:
                search_terms = json.load(file)
        else:
            search_terms = []

        # Add new search term
        search_terms.append(search_term)

        # Save search terms to file
        with open(search_terms_file, "w") as file:
            json.dump(search_terms, file)

    def load_user_info(self):
        # Load user info
        if os.path.exists(self.user_info_file):
            with open(self.user_info_file, "r") as file:
                self.user_info = json.load(file)
        else:
            self.user_info = {}

    def change_language(self):
        language = self.language_combo_box.currentText()
        if language == "English":
            self.translator.load("translations/en.qm")
        elif language == "Turkish":
            self.translator.load("translations/tr.qm")
            QApplication.instance().installTranslator(self.translator)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArchBrowserWindow()
    window.show()
    sys.exit(app.exec())
