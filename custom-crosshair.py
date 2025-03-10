import sys
from PyQt6.QtWidgets import QApplication, QLabel, QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QComboBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QShortcut, QKeySequence

class CrosshairApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Custom Crosshair Overlay")
        self.setGeometry(100, 100, 200, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        
        self.crosshair_label = QLabel(self)
        self.crosshair_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.crosshair_label)
        
        self.load_button = QPushButton("Load Crosshair")
        self.load_button.clicked.connect(self.load_crosshair)
        self.button_layout.addWidget(self.load_button)
        
        self.lock_button = QPushButton("🔒")
        self.lock_button.setCheckable(True)
        self.lock_button.clicked.connect(self.toggle_lock)
        self.button_layout.addWidget(self.lock_button)
        
        self.recenter_button = QPushButton("🔄️")
        self.recenter_button.clicked.connect(self.recenter_crosshair)
        self.button_layout.addWidget(self.recenter_button)
        
        self.resize_dropdown = QComboBox()
        self.resize_dropdown.addItems(["50 px", "75 px", "100 px", "150 px", "200 px", "300 px", "400 px", "500 px"])
        self.resize_dropdown.currentIndexChanged.connect(self.resize_crosshair)
        self.button_layout.addWidget(self.resize_dropdown)
        
        self.close_button = QPushButton("❌")
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(self.button_layout)
        self.setLayout(main_layout)
        self.drag_position = QPoint()
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        self.shortcut.activated.connect(self.toggle_ui_visibility)

        self.ui_visible = True
        self.locked = False
        self.original_pixmap = None
        
    def load_crosshair(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            self.update_crosshair_size()
            self.recenter_crosshair()
            
    def resize_crosshair(self):
        self.update_crosshair_size()
        self.update_toolbar_size()
        
    def update_crosshair_size(self):
        if self.original_pixmap:
            size = int(self.resize_dropdown.currentText().split()[0])
            scaled_pixmap = self.original_pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.crosshair_label.setPixmap(scaled_pixmap)
            self.resize(size, size)
            self.update_toolbar_size()
    
    def toggle_lock(self):
        self.locked = not self.locked
    
    def toggle_ui_visibility(self):
        self.ui_visible = not self.ui_visible
        self.load_button.setVisible(self.ui_visible)
        self.lock_button.setVisible(self.ui_visible)
        self.close_button.setVisible(self.ui_visible)
        self.resize_dropdown.setVisible(self.ui_visible)
        self.recenter_button.setVisible(self.ui_visible)
        
    def recenter_crosshair(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2
        self.move(center_x, center_y)
        
    def update_toolbar_size(self):
        toolbar_width = self.width()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        for i in range(self.button_layout.count()):
            self.button_layout.itemAt(i).widget().setMinimumWidth(toolbar_width // self.button_layout.count())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.locked:
            self.drag_position = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self.locked:
            self.move(event.globalPosition().toPoint() - self.drag_position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CrosshairApp()
    window.show()
    sys.exit(app.exec())
