import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QDesktopWidget, QTextEdit, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont, QImage, QFontMetrics
from PyQt5.QtCore import QObject, Qt, QPoint, QThread, pyqtSignal
from PIL import Image, ImageQt, ImageFilter, ImageOps
from PyQt5.uic import loadUi
import numpy as np
import os
PATH = os.path.dirname(os.path.realpath(__file__)) + "/"

class ImageOCR_Thread(QThread):
    send_image = pyqtSignal(QImage)
    extracted_text = pyqtSignal(str)
    def __init__(self, img, lang):
        super().__init__()
        self.img = img
        self.lang = lang
    
    def preprocess_image(self, img):
        # Convert to grayscale
        gray = img.convert('L')
        
        # Resize image
        width, height = gray.size
        new_width = int(width * 5)
        new_height = int(height * 5)
        resized = gray.resize((new_width, new_height), Image.LANCZOS)
        
        return resized

    def run(self):
        import pytesseract
        tessdata_prefix = os.path.expanduser('~/tessdata')
        os.environ['TESSDATA_PREFIX'] = tessdata_prefix
        preprocessed_img = self.preprocess_image(self.img)
        custom_oem_psm_config = r'--oem 3 --psm 3'
        text_output = pytesseract.image_to_string(preprocessed_img, lang=self.lang, config=custom_oem_psm_config)
        self.extracted_text.emit(text_output.strip())


class ImageClipboardViewer(QMainWindow):
    image_label: QLabel
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Image Clipboard Viewer")
        loadUi(PATH + "load.ui", self)
        self.scale_factor = 1
        self.update_image()

    def update_image(self):
        clipboard = QApplication.clipboard()

        mime_data = clipboard.mimeData()
        if mime_data.hasImage():
            image = mime_data.imageData()
            pixmap = QPixmap.fromImage(image)
            pixmap = pixmap.scaled(int(pixmap.width() * self.scale_factor), int(pixmap.height() * self.scale_factor), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
        else:
            self.image_label.setText("There is no Image to preview")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        elif event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_image()
        
        elif event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            self.get_text("ara")
        
        elif event.key() == Qt.Key_E and event.modifiers() == Qt.ControlModifier:
            self.get_text("eng")
        
        if event.key() == Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            self.scale_factor +=0.1
            self.update_image()
        
        if event.key() == Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            self.scale_factor -=0.1
            self.update_image()
        
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_Plus:
                self.adjustOpacity(0.1)  # Increase opacity by 10%
            elif event.key() == Qt.Key_Minus:
                self.adjustOpacity(-0.1)  # Decrease opacity by 10%

    def adjustOpacity(self, delta):
        opacity = self.windowOpacity() + delta
        opacity = max(0.1, min(opacity, 1.0))  # Ensure opacity is between 0.1 and 1.0
        self.setWindowOpacity(opacity)
    
    def get_text(self, lang):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            qt_image = mime_data.imageData()
            pil_image = ImageQt.fromqpixmap(qt_image)
            self.ocr_thread = ImageOCR_Thread(pil_image, lang)
            self.ocr_thread.extracted_text.connect(self.update_text)
            self.ocr_thread.start()

    def update_text(self, text):
        textEdit = QTextEdit(self)
        textEdit.setText(text)
        font_metrics = QFontMetrics(textEdit.font())
        text_height = font_metrics.height() * textEdit.document().lineCount()
        textEdit.setFixedHeight(text_height)
        self.centralWidget().layout().addWidget(textEdit)

    def save_image(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            image = mime_data.imageData()
            pixmap = QPixmap.fromImage(image)
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", " ~/Documents/", "Images (*.png *.jpg *.bmp)", options=options)
            if file_path:
                pixmap.save(file_path)
        else:
            self.image_label.setText("There is no Image to save")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageClipboardViewer()
    viewer.show()
    sys.exit(app.exec_())

