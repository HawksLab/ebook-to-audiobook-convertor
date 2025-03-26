from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal
import shutil

class MainWindowController:
    def __init__(self, ui, music_player_service, tts_service, parser_service):
        self.ui = ui
        self.music_player_service = music_player_service
        self.tts_service = tts_service
        self.parser_service = parser_service
        self.audio_paths = None
        self.merged_audio_path = None

        self.isAudioPlaying = False

        self.ui.convertButton.clicked.connect(self.convert_text_to_audio)
        self.ui.playButton.clicked.connect(self.play_audio)
        self.ui.streamButton.clicked.connect(self.stream_audio)
        self.ui.playMediaButton.clicked.connect(self.play_audio_toggle)
        self.ui.uploadButton.clicked.connect(self.upload_ebook)
        self.ui.saveButton.clicked.connect(self.save_audio)
        self.ui.openAction.triggered.connect(self.upload_ebook)
        self.ui.saveAction.triggered.connect(self.save_audio)
        self.ui.actionExit.triggered.connect(QtWidgets.QApplication.quit)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.music_player_service.player.positionChanged.connect(self.update_slider)
        self.music_player_service.player.durationChanged.connect(self.set_slider_range)
        self.ui.horizontalSlider.sliderMoved.connect(self.slider_moved)
        self.ui.horizontalSlider.sliderReleased.connect(self.slider_released)
    
    def show_about(self):
        about_dialog = QtWidgets.QMessageBox()
        about_dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        about_dialog.setWindowTitle("About")
        about_dialog.setText("Abook Convertor is a simple application that converts e-books to audio-books")
        about_dialog.setInformativeText('Product of <a href="https://github.com/HawksLab">Hawks Lab</a>')
        about_dialog.setTextFormat(QtCore.Qt.TextFormat.RichText)
        about_dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        about_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        about_dialog.exec()

    def stream_audio(self):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
        error_dialog.setWindowTitle("W.I.P")
        error_dialog.setText("Work in Progress")
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    def convert_text_to_audio(self):
        if self.ui.plainTextEdit.toPlainText() == "":
            print("No text to convert")
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("No text to convert")
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            error_dialog.exec()
            return
        self.audio_paths = self.tts_service.generate(self,
            self.ui.plainTextEdit.toPlainText(),
            self.ui.comboBox.currentText(),
        )

    def play_audio_toggle(self):
        if self.isAudioPlaying:
            self.music_player_service.pause()
            self.isAudioPlaying = False
        else:
            self.music_player_service.resume()
            self.isAudioPlaying = True
    
    def play_audio(self):
        if self.merged_audio_path:
            self.music_player_service.play(self.merged_audio_path)
        else:
            print("No audio to play") # Todo: add error popup here
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("No audio to play")
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            error_dialog.exec()

    def upload_ebook(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.ui.widget, "Open E-Book", "", "E-Book Files (*.pdf *.epub)")
        class LoadTextWorker(QThread):
            progress = pyqtSignal(str)
            finished_parsing = pyqtSignal(str)

            def __init__(self, parser_service, file_path):
                super().__init__()
                self.file_path = file_path
                self.parser_service = parser_service

            def run(self):
                parsed_text = self.parser_service.parse(self.file_path)
                self.finished_parsing.emit(parsed_text)

        if file_path:
            def on_finished(parsed_text):
                self.ui.plainTextEdit.setPlainText(parsed_text)

            self.worker = LoadTextWorker(self.parser_service, file_path)
            self.worker.finished_parsing.connect(lambda text: on_finished(text))
            self.worker.start()
    
    def save_audio(self):
        if self.merged_audio_path:
            file_dialog = QtWidgets.QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self.ui.widget, "Save Audio", "", "Audio Files (*.wav)")
            if file_path:
                shutil.copy(self.merged_audio_path, file_path)
        else:
            print("No audio to save")
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("No audio to save")
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            error_dialog.exec()
    
    def update_slider(self, position):
        self.ui.horizontalSlider.setValue(position)

    def set_slider_range(self, duration):
        self.ui.horizontalSlider.setRange(0, duration)

    def slider_moved(self, position):
        self.isSliderBeingMoved = True
        self.music_player_service.player.setPosition(position)

    def slider_released(self):
        self.isSliderBeingMoved = False