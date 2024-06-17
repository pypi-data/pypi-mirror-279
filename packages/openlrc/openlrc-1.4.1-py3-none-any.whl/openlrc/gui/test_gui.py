#  Copyright (C) 2024. Hao Zheng
#  All rights reserved.
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                               QHBoxLayout, QFileDialog, QCheckBox, QComboBox, QTextEdit, QSlider)
from PySide6.QtCore import Qt

class TranscriptionTranslationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # File Selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel('Selected Files:')
        self.file_display = QTextEdit()
        self.file_display.setReadOnly(True)
        self.browse_button = QPushButton('Browse')
        self.browse_button.clicked.connect(self.browse_files)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_display)
        file_layout.addWidget(self.browse_button)

        # Language Options
        lang_layout = QHBoxLayout()
        self.src_lang_label = QLabel('Source Language:')
        self.src_lang_combo = QComboBox()
        self.src_lang_combo.addItem('Auto-detect')

        self.target_lang_label = QLabel('Target Language:')
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItem('Mandarin Chinese')

        lang_layout.addWidget(self.src_lang_label)
        lang_layout.addWidget(self.src_lang_combo)
        lang_layout.addWidget(self.target_lang_label)
        lang_layout.addWidget(self.target_lang_combo)

        # Translation Options
        trans_options_layout = QVBoxLayout()
        self.skip_trans_check = QCheckBox('Skip Translation')
        self.noise_suppress_check = QCheckBox('Noise Suppress')
        self.bilingual_sub_check = QCheckBox('Bilingual Subtitles')
        self.noise_suppress_slider = QSlider(Qt.Horizontal)
        self.noise_suppress_slider.setRange(0, 100)
        self.noise_suppress_slider.setValue(50)
        self.noise_suppress_slider.setEnabled(False)

        self.noise_suppress_check.toggled.connect(self.noise_suppress_slider.setEnabled)

        trans_options_layout.addWidget(self.skip_trans_check)
        trans_options_layout.addWidget(self.noise_suppress_check)
        trans_options_layout.addWidget(self.noise_suppress_slider)
        trans_options_layout.addWidget(self.bilingual_sub_check)

        # Compute Options
        compute_layout = QVBoxLayout()
        self.whisper_model_label = QLabel('Whisper Model:')
        self.whisper_model_combo = QComboBox()
        self.whisper_model_combo.addItems(['large-v3', 'tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large-v1', 'large-v2', 'distill-large-v3'])

        self.compute_type_label = QLabel('Compute Type:')
        self.compute_type_combo = QComboBox()
        self.compute_type_combo.addItems(['float16', 'int8', 'int8_float16', 'int16', 'float32'])

        self.chatbot_model_label = QLabel('Chatbot Model:')
        self.chatbot_model_combo = QComboBox()
        self.chatbot_model_combo.addItems(['gpt-3.5-turbo', 'gpt-4-0125-preview', 'gpt-4-turbo-preview', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'])

        compute_layout.addWidget(self.whisper_model_label)
        compute_layout.addWidget(self.whisper_model_combo)
        compute_layout.addWidget(self.compute_type_label)
        compute_layout.addWidget(self.compute_type_combo)
        compute_layout.addWidget(self.chatbot_model_label)
        compute_layout.addWidget(self.chatbot_model_combo)

        # Advanced Options
        advanced_layout = QVBoxLayout()
        self.asr_options_button = QPushButton('ASR Options')
        self.vad_options_button = QPushButton('VAD Options')
        self.preprocess_options_button = QPushButton('Preprocess Options')

        advanced_layout.addWidget(self.asr_options_button)
        advanced_layout.addWidget(self.vad_options_button)
        advanced_layout.addWidget(self.preprocess_options_button)

        # Proxy Settings
        proxy_layout = QHBoxLayout()
        self.proxy_label = QLabel('Proxy URL:')
        self.proxy_input = QLineEdit()

        proxy_layout.addWidget(self.proxy_label)
        proxy_layout.addWidget(self.proxy_input)

        # Translation Execution
        exec_layout = QHBoxLayout()
        self.run_button = QPushButton('Run')
        self.clear_button = QPushButton('Clear')

        exec_layout.addWidget(self.run_button)
        exec_layout.addWidget(self.clear_button)

        # Status and Logs
        self.status_label = QLabel('Status:')
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(file_layout)
        main_layout.addLayout(lang_layout)
        main_layout.addLayout(trans_options_layout)
        main_layout.addLayout(compute_layout)
        main_layout.addLayout(advanced_layout)
        main_layout.addLayout(proxy_layout)
        main_layout.addLayout(exec_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.status_display)

        self.setLayout(main_layout)
        self.setWindowTitle('Transcription and Translation Tool')

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select Audio/Video Files', '', 'Audio/Video Files (*.mp3 *.mp4 *.wav *.avi)')
        if files:
            self.file_display.setPlainText('\n'.join(files))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = TranscriptionTranslationGUI()
    gui.show()
    sys.exit(app.exec())
