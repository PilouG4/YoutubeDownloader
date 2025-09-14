import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QFileDialog, QCheckBox, QComboBox
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from download import Download


class DownloadWorker(QThread):
    finished = pyqtSignal(bool, str)  # succès/erreur + message

    def __init__(self, url, format, resolution, playlist, directory):
        super().__init__()
        self.url = url
        self.format = format
        self.resolution = resolution
        self.playlist = playlist
        self.directory = directory

    def run(self):
        try:
            d = Download(
                url=self.url,
                format=self.format,
                resolution=self.resolution,
                Playlist=self.playlist,
                dir=self.directory
            )
            d.download()
            self.finished.emit(True, "Téléchargé ✅")
        except Exception as e:
            self.finished.emit(False, f"Erreur : {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Youtube Downloader")
        self.setGeometry(0, 0, 800, 600)
        self.setWindowIcon(QIcon("YoutubeDownloader.png"))

        # Widget central et layout principal
        central_widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        # Label de bienvenue
        label = QLabel("Bienvenue sur Youtube Downloader!")
        label.setFont(QFont("Arial", 16))
        label.setStyleSheet("color : #b31559; font-weight : bold; text-decoration : underline;")
        label.setAlignment(Qt.AlignCenter)

        # Image
        image_label = QLabel()
        pixmap = QPixmap("YoutubeDownloader.png")
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(100, 100)
        image_label.setAlignment(Qt.AlignCenter)

        # Checkbox Video
        self.checkbox_video = QCheckBox("Video")
        self.checkbox_video.setStyleSheet("font-size : 20px;")

        # Checkbox Audio
        self.checkbox_audio = QCheckBox("Audio")
        self.checkbox_audio.setStyleSheet("font-size : 20px;")

        # Line Edit URL
        self.line_edit_url = QLineEdit(self)
        self.line_edit_url.setStyleSheet(
            "background-color : #b31559; font-size : 14px; color : white; font-weight : bold;"
            "border-radius : 10px; padding : 5px; font-style : italic;"
        )
        self.line_edit_url.setPlaceholderText("Entrez le lien de la vidéo YouTube ici")

        # Directory button
        self.dir_button = QPushButton("Choisir un dossier")
        self.dir_button.setStyleSheet(
            "background-color : #b31559; font-size : 14px; color : white; font-weight : bold;"
            "border-radius : 10px; padding : 5px;"
        )
        self.dir_button.clicked.connect(self.choose_directory)

        # Directory line edit
        self.dir_line_edit = QLineEdit(self)
        self.dir_line_edit.setStyleSheet(
            "background-color : #b31559; font-size : 14px; color : white; font-weight : bold;"
            "border-radius : 10px; padding : 5px; font-style : italic;"
        )
        self.dir_line_edit.setPlaceholderText("Dossier de téléchargement")

        # Resolution combobox
        self.combobox_resolution = QComboBox(self)
        for res in ["4K", "2K", "1080p", "720p", "480p", "360p"]:
            self.combobox_resolution.addItem(res)
        self.combobox_resolution.setCurrentIndex(2)

        # Bouton
        self.button = QPushButton("Télécharger")
        self.button.setStyleSheet(
            "background-color : #b31559; font-size : 14px; color : white; font-weight : bold;"
            "border-radius : 10px; padding : 5px;"
        )
        self.button.clicked.connect(self.download_click)

        # Layout horizontal
        hbox = QHBoxLayout()
        hbox.addWidget(self.checkbox_video)
        hbox.addWidget(self.checkbox_audio)
        hbox.addWidget(self.combobox_resolution)
        hbox.addWidget(self.line_edit_url)
        hbox.addWidget(self.dir_button)

        # Ajout au layout
        vbox.addWidget(label)
        vbox.addWidget(image_label)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dir_line_edit)
        vbox.addWidget(self.button)
        vbox.addStretch()

        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def get_format(self):
        if self.checkbox_video.isChecked() and self.checkbox_audio.isChecked():
            return "video+audio"
        elif self.checkbox_video.isChecked():
            return "video"
        elif self.checkbox_audio.isChecked():
            return "audio"
        return None

    def download_click(self):
        format = self.get_format()
        url = self.line_edit_url.text().strip()

        if not url:
            self.set_button_message("Veuillez entrer une URL", "Télécharger")
            return

        if not format:
            self.set_button_message("Veuillez sélectionner un format", "Télécharger")
            return

        # Résolution
        res_text = self.combobox_resolution.currentText()
        if "K" in res_text:
            resolution = int(float(res_text.replace("K", "")) * 1000)
        else:
            resolution = int(res_text.replace("p", ""))

        # UI → état en cours
        self.button.setText("Téléchargement en cours...")
        self.button.setEnabled(False)

        # Worker thread
        self.worker = DownloadWorker(
            url=url,
            format=format,
            resolution=resolution,
            playlist=False,
            directory=self.dir_line_edit.text() or os.path.expanduser("~/Downloads")
        )
        self.worker.finished.connect(self.on_download_finished)
        self.worker.start()

    def on_download_finished(self, success, message):
        self.set_button_message(message, "Télécharger")

    def set_button_message(self, temp_text, reset_text, delay=2000):
        self.button.setText(temp_text)
        self.button.setEnabled(True)
        QTimer.singleShot(delay, lambda: self.button.setText(reset_text))

    def choose_directory(self):
        path = os.getenv('HOME') or ""
        fname = QFileDialog.getExistingDirectory(self, 'Choisir un dossier', os.path.join(path, "Documents"))
        if fname:
            self.dir_line_edit.setText(fname)
        return fname


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
