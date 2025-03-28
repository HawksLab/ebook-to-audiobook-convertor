from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QTextEdit, QComboBox, 
                            QSlider, QProgressBar, QSplitter, QFrame, QScrollArea,
                            QStackedWidget)
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QAction, QPixmap, QFontDatabase
from PyQt6.QtCore import Qt, QSize, QUrl, QTimer
from app.constants import TTS_VOICES
from app.controller.main_window_controller import MainWindowController
import sys

class Ui_MainWindow(QMainWindow):
    def __init__(self, music_player_service, tts_service, parser_service):
        super().__init__()
        self.setWindowTitle("Narratify")
        self.setMinimumSize(1000, 700)
        
        # Initialize variables
        self.current_file = None
        self.is_playing = False
        self.is_dark_mode = True
        self.music_player_service = music_player_service
        self.tts_service = tts_service
        self.parser_service = parser_service
        
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        self.apply_theme()

        # Attach controller
        self.controler = MainWindowController(self, music_player_service, tts_service, parser_service)
        
    def setup_menu(self):
        # Create menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        self.open_action = QAction("Open eBook", self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)
        
        self.save_action = QAction("Save Audiobook", self)
        self.save_action.setShortcut("Ctrl+S")
        file_menu.addAction(self.save_action)
        
        file_menu.addSeparator()
        
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(self.exit_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        
        self.theme_action = QAction("Toggle Theme", self)
        self.theme_action.setShortcut("Ctrl+T")
        view_menu.addAction(self.theme_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        self.about_action = QAction("About", self)
        help_menu.addAction(self.about_action)
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header with title and upload button
        header_layout = QHBoxLayout()
        
        title_label = QLabel("NARRATIFY")
        title_label.setObjectName("app-title")
        title_label.setFont(QFont("Courier New", 24, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.upload_btn = QPushButton("LOAD EBOOK")
        self.upload_btn.setObjectName("retro-button")
        self.upload_btn.setMinimumSize(150, 40)
        header_layout.addWidget(self.upload_btn)
        
        main_layout.addLayout(header_layout)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Left panel - Text content
        left_panel = QWidget()
        left_panel.setObjectName("retro-panel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        text_header = QLabel("TEXT DISPLAY")
        text_header.setObjectName("retro-header")
        text_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(text_header)
        
        # Text area with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("scroll-area")
        
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        
        self.text_edit = QTextEdit()
        # self.text_edit.setReadOnly(True)
        self.text_edit.setMinimumWidth(400)
        self.text_edit.setObjectName("retro-text")
        self.text_edit.setPlaceholderText("Waiting for text input...")
        text_layout.addWidget(self.text_edit)
        
        scroll_area.setWidget(text_container)
        left_layout.addWidget(scroll_area)
        
        # Right panel - Controls
        right_panel = QWidget()
        right_panel.setObjectName("retro-panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        # Stacked widget for different states
        self.stacked_widget = QStackedWidget()
        
        # Page 1: Initial state
        initial_page = QWidget()
        initial_page.setObjectName("retro-screen")
        initial_layout = QVBoxLayout(initial_page)
        initial_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        upload_icon_label = QLabel("📼")
        upload_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_icon_label.setStyleSheet("background: transparent;")
        upload_icon_label.setFont(QFont("Courier New", 48))
        initial_layout.addWidget(upload_icon_label)
        
        upload_text = QLabel("INSERT DISK TO CONTINUE")
        upload_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upload_text.setObjectName("retro-text")
        upload_text.setFont(QFont("Courier New", 14))
        initial_layout.addWidget(upload_text)
        
        self.upload_btn2 = QPushButton("LOAD EBOOK")
        self.upload_btn2.setObjectName("retro-button-primary")
        self.upload_btn2.setMinimumSize(200, 50)
        self.upload_btn2.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        initial_layout.addWidget(self.upload_btn2, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.stacked_widget.addWidget(initial_page)
        
        # Page 2: Conversion options
        conversion_page = QWidget()
        conversion_page.setObjectName("retro-screen")
        conversion_layout = QVBoxLayout(conversion_page)
        
        options_header = QLabel("CONFIGURATION")
        options_header.setObjectName("retro-header")
        options_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        options_header.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
        conversion_layout.addWidget(options_header)
        
        # Voice selection
        voice_frame = QFrame()
        voice_frame.setObjectName("retro-frame")
        voice_layout = QVBoxLayout(voice_frame)
        
        voice_title = QLabel("VOICE SELECT")
        voice_title.setObjectName("retro-label")
        voice_title.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        voice_layout.addWidget(voice_title)
        
        voice_select_layout = QHBoxLayout()
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["SYNTH-1", "RETRO-WAVE", "8-BIT", 
                                  "ARCADE", "VAPORWAVE"])
        self.voice_combo.setMinimumHeight(40)
        self.voice_combo.setFont(QFont("Courier New", 10))
        self.voice_combo.setObjectName("retro-combo")
        
        self.preview_btn = QPushButton("TEST")
        self.preview_btn.setObjectName("retro-button")
        self.preview_btn.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        
        voice_select_layout.addWidget(self.voice_combo)
        voice_select_layout.addWidget(self.preview_btn)
        voice_layout.addLayout(voice_select_layout)
        
        conversion_layout.addWidget(voice_frame)
        
        # Speed selection
        speed_frame = QFrame()
        speed_frame.setObjectName("retro-frame")
        speed_layout = QVBoxLayout(speed_frame)
        
        speed_title = QLabel("PLAYBACK SPEED")
        speed_title.setObjectName("retro-label")
        speed_title.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        speed_layout.addWidget(speed_title)
        
        speed_slider_layout = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(100)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(25)
        self.speed_slider.setObjectName("retro-slider")
        
        self.speed_value_label = QLabel("1.0X")
        self.speed_value_label.setFont(QFont("Courier New", 10))
        
        speed_slider_layout.addWidget(QLabel("0.5X"))
        speed_slider_layout.addWidget(self.speed_slider)
        speed_slider_layout.addWidget(QLabel("2.0X"))
        speed_layout.addLayout(speed_slider_layout)
        speed_layout.addWidget(self.speed_value_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        conversion_layout.addWidget(speed_frame)
        
        
        conversion_layout.addSpacing(20)
        
        # Convert button
        self.convert_btn = QPushButton("CONVERT TO AUDIO")
        self.convert_btn.setObjectName("retro-button-primary")
        self.convert_btn.setMinimumHeight(60)
        self.convert_btn.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        conversion_layout.addWidget(self.convert_btn)
        
        conversion_layout.addStretch()
        
        self.stacked_widget.addWidget(conversion_page)
        
        # Page 3: Player
        player_page = QWidget()
        player_page.setObjectName("retro-screen")
        player_layout = QVBoxLayout(player_page)
        
        player_header = QLabel("AUDIO PLAYER")
        player_header.setObjectName("retro-header")
        player_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        player_header.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
        player_layout.addWidget(player_header)
        
        # Audio visualization (placeholder)
        visualization_frame = QFrame()
        visualization_frame.setMinimumHeight(120)
        visualization_frame.setObjectName("visualization-frame")
        player_layout.addWidget(visualization_frame)
        
        # Player controls
        controls_frame = QFrame()
        controls_frame.setObjectName("retro-frame")
        controls_layout = QVBoxLayout(controls_frame)
        
        # Time display
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setFont(QFont("Courier New", 12))
        self.current_time_label.setObjectName("time-display")
        self.total_time_label = QLabel("00:00")
        self.total_time_label.setFont(QFont("Courier New", 12))
        self.total_time_label.setObjectName("time-display")
        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time_label)
        controls_layout.addLayout(time_layout)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(100)
        self.progress_slider.setObjectName("retro-slider")
        controls_layout.addWidget(self.progress_slider)
        
        # Playback buttons
        playback_layout = QHBoxLayout()
        playback_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.prev_btn = QPushButton("◀◀")
        self.prev_btn.setObjectName("retro-button-control")
        self.prev_btn.setFixedSize(60, 60)
        self.prev_btn.setFont(QFont("Courier New", 16))
        
        self.play_btn = QPushButton("▶")
        self.play_btn.setObjectName("retro-button-play")
        self.play_btn.setFixedSize(80, 80)
        self.play_btn.setFont(QFont("Courier New", 24))
        
        self.next_btn = QPushButton("▶▶")
        self.next_btn.setObjectName("retro-button-control")
        self.next_btn.setFixedSize(60, 60)
        self.next_btn.setFont(QFont("Courier New", 16))
        
        playback_layout.addStretch()
        playback_layout.addWidget(self.prev_btn)
        playback_layout.addWidget(self.play_btn)
        playback_layout.addWidget(self.next_btn)
        playback_layout.addStretch()
        
        controls_layout.addLayout(playback_layout)
        
        player_layout.addWidget(controls_frame)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("SAVE")
        self.save_btn.setObjectName("retro-button")
        self.save_btn.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        
        self.new_conversion_btn = QPushButton("NEW")
        self.new_conversion_btn.setObjectName("retro-button")
        self.new_conversion_btn.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        
        action_layout.addWidget(self.save_btn)
        action_layout.addWidget(self.new_conversion_btn)
        
        player_layout.addLayout(action_layout)
        player_layout.addStretch()
        
        self.stacked_widget.addWidget(player_page)
        
        # Page 4: Conversion progress
        progress_page = QWidget()
        progress_page.setObjectName("retro-screen")
        progress_layout = QVBoxLayout(progress_page)
        progress_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        progress_label = QLabel("PROCESSING...")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_label.setObjectName("retro-header")
        progress_label.setFont(QFont("Courier New", 18, QFont.Weight.Bold))
        progress_layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimumWidth(400)
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setObjectName("retro-progress")
        progress_layout.addWidget(self.progress_bar)
        
        progress_detail = QLabel("PLEASE WAIT... DO NOT TURN OFF SYSTEM")
        progress_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_detail.setObjectName("retro-text")
        progress_detail.setFont(QFont("Courier New", 12))
        progress_layout.addWidget(progress_detail)
        
        self.stacked_widget.addWidget(progress_page)
        
        right_layout.addWidget(self.stacked_widget)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([500, 500])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("SYSTEM READY")
    
    def apply_theme(self):
        # Apply minimalist retro theme
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: #e0e0e0;
                    font-family: 'Courier New', monospace;
                }
                QMenuBar {
                    background-color: #121212;
                    color: #e0e0e0;
                    border-bottom: 1px solid #404040;
                }
                QMenuBar::item:selected {
                    background-color: #404040;
                }
                QMenu {
                    background-color: #121212;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                }
                QMenu::item:selected {
                    background-color: #404040;
                }
                QPushButton {
                    border: 1px solid #404040;
                    border-radius: 0px;
                    padding: 8px 16px;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                }
                QPushButton:hover {
                    background-color: #2a2a2a;
                }
                QPushButton#retro-button {
                    border: 1px solid #404040;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                }
                QPushButton#retro-button:hover {
                    background-color: #2a2a2a;
                }
                QPushButton#retro-button-primary {
                    border: 1px solid #505050;
                    background-color: #404040;
                    color: #ffffff;
                    font-weight: bold;
                }
                QPushButton#retro-button-primary:hover {
                    background-color: #505050;
                }
                QPushButton#retro-button-control {
                    border: 1px solid #404040;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                }
                QPushButton#retro-button-control:hover {
                    background-color: #2a2a2a;
                }
                QPushButton#retro-button-play {
                    border: 1px solid #505050;
                    background-color: #404040;
                    color: #ffffff;
                }
                QPushButton#retro-button-play:hover {
                    background-color: #505050;
                }
                QTextEdit {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                    border-radius: 0px;
                    padding: 8px;
                    selection-background-color: #505050;
                    font-family: 'Courier New', monospace;
                    font-size: 12pt;
                }
                QTextEdit#retro-text {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                    border-radius: 0px;
                    padding: 20px;
                    line-height: 1.5;
                }
                QComboBox {
                    border: 1px solid #404040;
                    border-radius: 0px;
                    padding: 4px 8px;
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                }
                QComboBox#retro-combo {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                    border-radius: 0px;
                    padding: 4px 8px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 24px;
                }
                QComboBox QAbstractItemView {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                    selection-background-color: #505050;
                }
                QSlider::groove:horizontal {
                    height: 6px;
                    background: #404040;
                    border-radius: 0px;
                }
                QSlider::handle:horizontal {
                    background: #707070;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border: 1px solid #404040;
                    border-radius: 0px;
                }
                QProgressBar {
                    background-color: #1a1a1a;
                    color: #e0e0e0;
                    border: 1px solid #404040;
                    border-radius: 0px;
                    text-align: center;
                    font-weight: bold;
                }
                QProgressBar::chunk {
                    background-color: #505050;
                    border-radius: 0px;
                }
                QLabel#app-title {
                    color: #ffffff;
                    font-weight: bold;
                    font-size: 24px;
                }
                QLabel#retro-header {
                    color: #ffffff;
                    font-weight: bold;
                    font-size: 18px;
                }
                QLabel#retro-text {
                    color: #e0e0e0;
                }
                QLabel#retro-label {
                    color: #a0a0a0;
                    font-weight: bold;
                }
                QLabel#time-display {
                    color: #e0e0e0;
                    font-weight: bold;
                    background-color: #1a1a1a;
                    border: 1px solid #404040;
                    padding: 4px;
                }
                QFrame#visualization-frame {
                    background-color: #1a1a1a;
                    border: 1px solid #404040;
                    border-radius: 0px;
                }
                QScrollBar:vertical {
                    background-color: #1a1a1a;
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #404040;
                    min-height: 20px;
                    margin: 2px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QStatusBar {
                    background-color: #121212;
                    color: #a0a0a0;
                    border-top: 1px solid #404040;
                }
                QWidget#retro-panel {
                    background-color: #1a1a1a;
                    border: 1px solid #404040;
                    border-radius: 0px;
                }
                QWidget#retro-screen {
                    background-color: #1a1a1a;
                    border: 1px solid #404040;
                    border-radius: 0px;
                }
                QFrame#retro-frame {
                    background-color: #1a1a1a;
                    border: 1px solid #404040;
                    border-radius: 0px;
                    padding: 10px;
                    margin: 5px;
                }
                QScrollArea#scroll-area {
                    border: none;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #202020;
                    font-family: 'Courier New', monospace;
                }
                QMenuBar {
                    background-color: #f0f0f0;
                    color: #202020;
                    border-bottom: 1px solid #d0d0d0;
                }
                QMenuBar::item:selected {
                    background-color: #d0d0d0;
                }
                QMenu {
                    background-color: #f0f0f0;
                    color: #202020;
                    border: 1px solid #d0d0d0;
                }
                QMenu::item:selected {
                    background-color: #d0d0d0;
                }
                QPushButton {
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    padding: 8px 16px;
                    background-color: #e0e0e0;
                    color: #202020;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton#retro-button {
                    border: 1px solid #d0d0d0;
                    background-color: #e0e0e0;
                    color: #202020;
                }
                QPushButton#retro-button:hover {
                    background-color: #d0d0d0;
                }
                QPushButton#retro-button-primary {
                    border: 1px solid #a0a0a0;
                    background-color: #b0b0b0;
                    color: #ffffff;
                    font-weight: bold;
                }
                QPushButton#retro-button-primary:hover {
                    background-color: #a0a0a0;
                }
                QPushButton#retro-button-control {
                    border: 1px solid #d0d0d0;
                    background-color: #e0e0e0;
                    color: #202020;
                }
                QPushButton#retro-button-control:hover {
                    background-color: #d0d0d0;
                }
                QPushButton#retro-button-play {
                    border: 1px solid #a0a0a0;
                    background-color: #b0b0b0;
                    color: #ffffff;
                }
                QPushButton#retro-button-play:hover {
                    background-color: #a0a0a0;
                }
                QTextEdit {
                    background-color: #ffffff;
                    color: #202020;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    padding: 8px;
                    selection-background-color: #b0b0b0;
                    font-family: 'Courier New', monospace;
                    font-size: 12pt;
                }
                QTextEdit#retro-text {
                    background-color: #ffffff;
                    color: #202020;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    padding: 20px;
                    line-height: 1.5;
                }
                QComboBox {
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    padding: 4px 8px;
                    background-color: #e0e0e0;
                    color: #202020;
                }
                QComboBox#retro-combo {
                    background-color: #e0e0e0;
                    color: #202020;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    padding: 4px 8px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 24px;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    color: #202020;
                    border: 1px solid #d0d0d0;
                    selection-background-color: #b0b0b0;
                }
                QSlider::groove:horizontal {
                    height: 6px;
                    background: #d0d0d0;
                    border-radius: 0px;
                }
                QSlider::handle:horizontal {
                    background: #909090;
                    width: 16px;
                    height: 16px;
                    margin: -5px 0;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                }
                QProgressBar {
                    background-color: #ffffff;
                    color: #202020;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    text-align: center;
                    font-weight: bold;
                }
                QProgressBar::chunk {
                    background-color: #b0b0b0;
                    border-radius: 0px;
                }
                QLabel#app-title {
                    color: #202020;
                    font-weight: bold;
                    font-size: 24px;
                }
                QLabel#retro-header {
                    color: #202020;
                    font-weight: bold;
                    font-size: 18px;
                }
                QLabel#retro-text {
                    color: #202020;
                }
                QLabel#retro-label {
                    color: #505050;
                    font-weight: bold;
                }
                QLabel#time-display {
                    color: #202020;
                    font-weight: bold;
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    padding: 4px;
                }
                QFrame#visualization-frame {
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                }
                QScrollBar:vertical {
                    background-color: #e0e0e0;
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #b0b0b0;
                    min-height: 20px;
                    margin: 2px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QStatusBar {
                    background-color: #f0f0f0;
                    color: #505050;
                    border-top: 1px solid #d0d0d0;
                }
                QWidget#retro-panel {
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                }
                QWidget#retro-screen {
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                }
                QFrame#retro-frame {
                    background-color: #ffffff;
                    border: 1px solid #d0d0d0;
                    border-radius: 0px;
                    padding: 10px;
                    margin: 5px;
                }
                QScrollArea#scroll-area {
                    border: none;
                }
            """)
