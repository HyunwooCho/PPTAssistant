from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent, QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from pptassistant.engine import ProcessingOptions, process_presentation


class Worker(QThread):
    progress = Signal(int, int, str)
    log = Signal(str)
    completed = Signal()
    failed = Signal(str)

    def __init__(self, files: list[Path], options: ProcessingOptions) -> None:
        super().__init__()
        self.files = files
        self.options = options

    def run(self) -> None:
        try:
            total = len(self.files)
            for index, path in enumerate(self.files, start=1):
                self.progress.emit(index - 1, total, path.name)
                result = process_presentation(path, self.options)
                self.log.emit(f"[{path.name}]")
                for message in result.messages:
                    self.log.emit(f"  {message}")
                self.progress.emit(index, total, path.name)
            self.completed.emit()
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


class DropList(QListWidget):
    files_dropped = Signal(list)

    SUPPORTED_EXTENSIONS = {".pptx", ".potx"}

    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setMinimumHeight(150)
        self.setToolTip("Drop PPTX or POTX files here")

    def _has_valid_file(self, event: QDropEvent | QDragMoveEvent) -> bool:
        mime_data = event.mimeData()
        if not mime_data.hasUrls():
            return False
        return any(
            url.isLocalFile()
            and Path(url.toLocalFile()).suffix.lower() in self.SUPPORTED_EXTENSIONS
            for url in mime_data.urls()
        )

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        # print("Drag enter event")

        if self._has_valid_file(event):
            event.acceptProposedAction()
        else:
            event.ignore()

        # if event.mimeData().hasUrls():
        #     event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        # print("Drag move event")

        if self._has_valid_file(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        # print("Drop event")

        paths = [
            Path(url.toLocalFile())
            for url in event.mimeData().urls()
            if url.isLocalFile()
        ]

        valid = [
            path
            for path in paths
            if path.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]

        if valid:
            self.files_dropped.emit(valid)
            event.acceptProposedAction()
        else:
            event.ignore()
        # self.files_dropped.emit(valid)
        # event.acceptProposedAction()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.files: list[Path] = []
        self.worker: Worker | None = None
        self.setWindowTitle("PPT Assistant v3.0 by TENACE")
        self.resize(840, 680)
        # self.setAcceptDrops(True)
        self._build_ui()
        self._apply_style()
        self._check_admin_privileges()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        title = QLabel("PPT Assistant")
        title.setObjectName("Title")
        subtitle = QLabel("PowerPoint cleanup and style tools · by tenace")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.file_list = DropList()
        self.file_list.files_dropped.connect(self.add_files)
        layout.addWidget(self.file_list)

        file_buttons = QHBoxLayout()
        add_button = QPushButton("Add files")
        add_button.clicked.connect(self.choose_files)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_files)
        file_buttons.addWidget(add_button)
        file_buttons.addWidget(clear_button)
        file_buttons.addStretch()
        layout.addLayout(file_buttons)

        self.remove_proofing = QCheckBox("Remove red underlines and proofing metadata")
        self.remove_proofing.setChecked(True)
        self.normalize_fonts = QCheckBox("Normalize fonts to Pretendard")
        self.remove_notes = QCheckBox("Remove speaker notes")
        layout.addWidget(self.remove_proofing)
        layout.addWidget(self.normalize_fonts)
        layout.addWidget(self.remove_notes)

        self.run_button = QPushButton("Process presentations")
        self.run_button.setObjectName("PrimaryButton")
        self.run_button.clicked.connect(self.start_processing)
        layout.addWidget(self.run_button)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("Processing log")
        layout.addWidget(self.log, 1)

        self.setCentralWidget(root)

    def _apply_style(self) -> None:
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet(
            """
            QMainWindow { background: #f4f6f8; }
            QLabel#Title { font-size: 28px; font-weight: 700; color: #17202a; }
            QLabel#Subtitle { color: #667085; margin-bottom: 8px; }
            QListWidget, QPlainTextEdit {
                background: white; border: 1px solid #d0d5dd; border-radius: 10px;
                padding: 10px;
            }
            QPushButton {
                background: white; border: 1px solid #cbd5e1; border-radius: 8px;
                padding: 9px 16px;
            }
            QPushButton:hover { background: #eef2f6; }
            QPushButton#PrimaryButton {
                background: #005bac; color: white; border: none; font-weight: 600;
                padding: 12px;
            }
            QPushButton#PrimaryButton:hover { background: #004a8d; }
            QCheckBox { spacing: 9px; padding: 3px; }
            QProgressBar {
                border: 1px solid #d0d5dd; border-radius: 7px; text-align: center;
                background: white; height: 18px;
            }
            QProgressBar::chunk { background: #00a6d6; border-radius: 6px; }
            """
        )

    def _check_admin_privileges(self) -> None:
        try:
            import ctypes
            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            is_admin = False
        print(f"Administrator privileges: {is_admin}")

        if is_admin:
            QMessageBox.warning(
                self,
                "Administrator mode detected",
                "PPT Assistant is running with administrator privileges. Some features may not work correctly.\n\n"
                "Windows Explorer normally runs without administrator privileges, so if you want to use PPT Assistant with administrator privileges, "
                "so files may not be draggable from Explorer into this application.\n\n"
                "Close this application and run it normally, "
                "not with 'Run as administrator'.",
            )

    def choose_files(self) -> None:
        names, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PowerPoint files",
            "",
            "PowerPoint (*.pptx *.potx)",
        )
        self.add_files([Path(name) for name in names])

    def add_files(self, paths: list[Path]) -> None:
        known = {p.resolve() for p in self.files}
        for path in paths:
            resolved = path.resolve()
            if resolved not in known:
                self.files.append(resolved)
                self.file_list.addItem(str(resolved))
                known.add(resolved)

    def clear_files(self) -> None:
        self.files.clear()
        self.file_list.clear()
        self.log.clear()
        self.progress.setValue(0)

    def start_processing(self) -> None:
        if not self.files:
            QMessageBox.information(self, "PPT Assistant", "Add at least one PPTX file.")
            return

        options = ProcessingOptions(
            remove_proofing=self.remove_proofing.isChecked(),
            normalize_font=self.normalize_fonts.isChecked(),
            font_name="Pretendard",
            remove_notes=self.remove_notes.isChecked(),
        )
        self.run_button.setEnabled(False)
        self.log.appendPlainText("Starting processing...")
        self.worker = Worker(self.files, options)
        self.worker.progress.connect(self.on_progress)
        self.worker.log.connect(self.log.appendPlainText)
        self.worker.completed.connect(self.on_completed)
        self.worker.failed.connect(self.on_failed)
        self.worker.start()

    def on_progress(self, current: int, total: int, name: str) -> None:
        percent = int(current / total * 100) if total else 0
        self.progress.setValue(percent)
        self.progress.setFormat(f"{current}/{total} · {name}")

    def on_completed(self) -> None:
        self.progress.setValue(100)
        self.progress.setFormat("Completed")
        self.run_button.setEnabled(True)
        self.log.appendPlainText("All files completed.")
        QMessageBox.information(self, "PPT Assistant", "Processing completed.")

    def on_failed(self, message: str) -> None:
        self.run_button.setEnabled(True)
        self.log.appendPlainText(f"ERROR: {message}")
        QMessageBox.critical(self, "PPT Assistant", message)
