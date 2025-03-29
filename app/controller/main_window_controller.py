from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import shutil

class MainWindowController:
    def __init__(self, ui, music_player_service, tts_service, parser_service):
        self.ui = ui
        self.music_player_service = music_player_service
        self.tts_service = tts_service
        self.parser_service = parser_service
        self.audio_paths = None
        self.merged_audio_path = None
        self.speed_value = 1.0
        self.is_playing = False
        self.started = False

        self.isAudioPlaying = False

        # Menu
        self.ui.open_action.triggered.connect(self.open_file)
        self.ui.save_action.triggered.connect(self.save_file)
        self.ui.exit_action.triggered.connect(self.ui.close)
        self.ui.theme_action.triggered.connect(self.toggle_theme)
        self.ui.about_action.triggered.connect(self.show_about)

        # UI Elements
        self.ui.upload_btn.clicked.connect(self.open_file)
        self.ui.upload_btn2.clicked.connect(self.open_file)
        self.ui.preview_btn.clicked.connect(self.preview_voice)
        self.ui.convert_btn.clicked.connect(self.convert_to_audio)
        self.ui.play_btn.clicked.connect(self.toggle_playback)
        self.ui.prev_btn.clicked.connect(self.seek_backward)
        self.ui.next_btn.clicked.connect(self.seek_forward)
        self.ui.speed_slider.valueChanged.connect(self.update_speed_label)
        self.music_player_service.player.positionChanged.connect(self.update_slider)
        self.music_player_service.player.durationChanged.connect(self.set_slider_range)
        self.ui.progress_slider.sliderMoved.connect(self.slider_moved)
        self.ui.progress_slider.sliderReleased.connect(self.slider_released)

        # Actions
        self.ui.save_btn.clicked.connect(self.save_file)
        self.ui.new_conversion_btn.clicked.connect(self.reset_to_conversion)

        

        # self.ui.convertButton.clicked.connect(self.convert_text_to_audio)
        # self.ui.playButton.clicked.connect(self.play_audio)
        # self.ui.streamButton.clicked.connect(self.stream_audio)
        # self.ui.playMediaButton.clicked.connect(self.play_audio_toggle)
        # self.ui.uploadButton.clicked.connect(self.upload_ebook)
        # self.ui.saveButton.clicked.connect(self.save_audio)
        # self.ui.openAction.triggered.connect(self.upload_ebook)
        # self.ui.saveAction.triggered.connect(self.save_audio)
        # self.ui.actionExit.triggered.connect(QtWidgets.QApplication.quit)
        # self.ui.actionAbout.triggered.connect(self.show_about)
        # self.music_player_service.player.positionChanged.connect(self.update_slider)
        # self.music_player_service.player.durationChanged.connect(self.set_slider_range)
        # self.ui.horizontalSlider.sliderMoved.connect(self.slider_moved)
        # self.ui.horizontalSlider.sliderReleased.connect(self.slider_released)
    
    def toggle_theme(self):
        self.ui.is_dark_mode = not self.ui.is_dark_mode
        self.ui.apply_theme()

    def open_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.ui, "Open E-Book", "", "E-Book Files (*.pdf *.epub)")
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
                self.ui.text_edit.setText(parsed_text)
                self.ui.statusBar().showMessage(f"PARSED: {file_path}")
                self.ui.stacked_widget.setCurrentIndex(1)

            self.worker = LoadTextWorker(self.parser_service, file_path)
            self.worker.finished_parsing.connect(lambda text: on_finished(text))
            self.ui.statusBar().showMessage(f"PARSING: {file_path}")
            self.ui.text_edit.setPlainText("Parsing...")
            self.worker.start()
    
    def save_file(self):
        if self.merged_audio_path:
            file_dialog = QtWidgets.QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self.ui, "Save Audio", "", "Audio Files (*.wav)")
            if file_path:
                shutil.copy(self.merged_audio_path, file_path)
                self.ui.statusBar().showMessage(f"SAVED TO: {file_path}")
        else:
            print("No audio to save")
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("No audio to save")
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            error_dialog.exec()
    
    def update_speed_label(self):
        self.speed_value = self.ui.speed_slider.value() / 100
        self.ui.speed_value_label.setText(f"{self.speed_value:.1f}X")
    
    def preview_voice(self):
        voice = self.ui.voice_combo.currentText()
        # Simulate voice preview
        self.ui.statusBar().showMessage(f"TESTING: {voice}")
        QMessageBox.information(self.ui, "VOICE TEST", f"W.I.P")
        # QMessageBox.information(self.ui, "VOICE TEST", f"PLAYING {voice} VOICE SAMPLE")
    
    def convert_to_audio(self):
        if self.ui.text_edit.toPlainText() == "":
            print("No text to convert")
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("No text to convert")
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            error_dialog.exec()
            return
        
        # Switch to progress page
        self.ui.stacked_widget.setCurrentIndex(3)
        self.started = False
        self.ui.progress_bar.setValue(0)

        
        self.audio_paths = self.tts_service.generate(
            self,
            self.ui,
            self.ui.text_edit.toPlainText(),
            self.ui.voice_combo.currentText(),
            self.speed_value,
        )
    
    def toggle_playback(self):
        if not self.started and self.merged_audio_path:
            self.started = True
            self.music_player_service.play(self.merged_audio_path)
            self.ui.play_btn.setText("⏸")
            self.ui.statusBar().showMessage("PLAYING")
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.ui.play_btn.setText("⏸")
            self.music_player_service.resume()
            self.ui.statusBar().showMessage("PLAYING")
        else:
            self.ui.play_btn.setText("▶")
            self.music_player_service.pause()
            self.ui.statusBar().showMessage("PAUSED")
    
    def reset_to_conversion(self):
        self.ui.stacked_widget.setCurrentIndex(1)
    
    def show_about(self):
        QMessageBox.about(
            self.ui, 
            "ABOUT NARRATIFY",
            "NARRATIFY v1.0\n\nSimple application that converts e-books to audio-books\n\n© 2025 HAWKS LABS"
        )

    def update_slider(self, position):
        self.ui.current_time_label.setText(
            "{:02}:{:02}".format(int((position//1000) // 60), int((position//1000) % 60))
        )
        self.ui.progress_slider.setValue(position)
    
    def seek_forward(self):
        self.music_player_service.player.setPosition(self.ui.progress_slider.value() + 5000)
        self.music_player_service.player.play()

    def seek_backward(self):
        self.music_player_service.player.setPosition(self.ui.progress_slider.value() - 5000)
        self.music_player_service.player.play()

    def set_slider_range(self, duration):
        self.ui.progress_slider.setRange(0, duration)

    def slider_moved(self, position):
        self.isSliderBeingMoved = True
        self.music_player_service.player.setPosition(position)

    def slider_released(self):
        self.isSliderBeingMoved = False