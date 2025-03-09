import sys
from PyQt6.QtWidgets import QApplication, QLabel, QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QShortcut
from PyQt6.QtGui import QKeySequence

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
        
    def load_crosshair(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.crosshair_label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            self.crosshair_label.setStyleSheet("background: transparent;")
            
            # Center the window on the screen
            screen_geometry = QApplication.primaryScreen().geometry()
            center_x = (screen_geometry.width() - self.width()) // 2
            center_y = (screen_geometry.height() - self.height()) // 2
            self.move(center_x, center_y)
            
    def toggle_lock(self):
        self.locked = not self.locked
    
    def toggle_ui_visibility(self):
        self.ui_visible = not self.ui_visible
        self.load_button.setVisible(self.ui_visible)
        self.lock_button.setVisible(self.ui_visible)
        self.close_button.setVisible(self.ui_visible)
        
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
