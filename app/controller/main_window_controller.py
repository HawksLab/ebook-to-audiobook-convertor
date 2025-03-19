from PyQt6 import QtWidgets
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
        self.music_player_service.player.positionChanged.connect(self.update_slider)
        self.music_player_service.player.durationChanged.connect(self.set_slider_range)
        self.ui.horizontalSlider.sliderMoved.connect(self.slider_moved)
        self.ui.horizontalSlider.sliderReleased.connect(self.slider_released)
    
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
        self.audio_paths = self.tts_service.generate(
            self.ui.plainTextEdit.toPlainText(),
            self.ui.comboBox.currentText(),
        )
        self.merged_audio_path = self.music_player_service.concatinate(self.audio_paths)

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
        if file_path:
            text = self.parser_service.parse(file_path)
            self.ui.plainTextEdit.setPlainText(text)
    
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