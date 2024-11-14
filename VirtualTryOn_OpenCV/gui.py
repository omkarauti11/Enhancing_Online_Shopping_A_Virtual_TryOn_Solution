import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QFile, QTextStream
from processor import process_image, process_video_or_realtime  # Import methods from processor.py


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Virtual Dressing Room")
        self.setGeometry(100, 100, 600, 400)

        # Create layout for main window
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Add Try with Image section
        self.try_image_label = QLabel("Try with Image/Photo")
        self.try_image_button = QPushButton("Click here to try")
        self.try_image_button.clicked.connect(self.open_image_window)
        self.layout.addWidget(self.try_image_label)
        self.layout.addWidget(self.try_image_button)

        # Add Try with Video section
        self.try_video_label = QLabel("Try with Video")
        self.try_video_button = QPushButton("Click here to try")
        self.try_video_button.clicked.connect(self.open_video_window)
        self.layout.addWidget(self.try_video_label)
        self.layout.addWidget(self.try_video_button)

        # Add Try with Real-time Video Capture section
        self.try_realtime_label = QLabel("Try with Real-time Video Capture")
        self.try_realtime_button = QPushButton("Click here to try")
        self.try_realtime_button.clicked.connect(self.open_realtime_window)
        self.layout.addWidget(self.try_realtime_label)
        self.layout.addWidget(self.try_realtime_button)

        self.load_stylesheet()

    def load_stylesheet(self):
        """Load and apply the CSS stylesheet"""
        file = QFile("style.css")
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())

    @pyqtSlot()
    def open_image_window(self):
        self.image_window = TryWithImageWindow()
        self.image_window.show()

    @pyqtSlot()
    def open_video_window(self):
        self.video_window = TryWithVideoWindow()
        self.video_window.show()

    @pyqtSlot()
    def open_realtime_window(self):
        self.realtime_window = TryWithRealtimeWindow()
        self.realtime_window.show()


# Window for Try-On with Image
class TryWithImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Try-On with Image")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()

        # Field for selecting user image
        self.user_image_label = QLabel("Select Your Image:")
        self.user_image_field = QLineEdit()
        self.user_image_button = QPushButton("Browse")
        self.user_image_button.clicked.connect(self.select_user_image)
        self.layout.addWidget(self.user_image_label)
        self.layout.addWidget(self.user_image_field)
        self.layout.addWidget(self.user_image_button)

        # Field for selecting t-shirt image
        self.tshirt_image_label = QLabel("Select Your T-shirt Image:")
        self.tshirt_image_field = QLineEdit()
        self.tshirt_image_button = QPushButton("Browse")
        self.tshirt_image_button.clicked.connect(self.select_tshirt_image)
        self.layout.addWidget(self.tshirt_image_label)
        self.layout.addWidget(self.tshirt_image_field)
        self.layout.addWidget(self.tshirt_image_button)

        # Buttons for processing
        self.process_button = QPushButton("Start Processing")
        self.process_button.clicked.connect(self.start_processing)
        self.stop_button = QPushButton("Stop Processing")
        self.stop_button.clicked.connect(self.stop_processing)
        self.layout.addWidget(self.process_button)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            
            QLabel {
                color: #333333;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-bottom: 10px;
                background-color: white;
            }

            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 10px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #3e8e41;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
        """)

    def select_user_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select User Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.user_image_field.setText(file_name)

    def select_tshirt_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select T-shirt Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.tshirt_image_field.setText(file_name)

    def start_processing(self):
        user_image = self.user_image_field.text()
        tshirt_image = self.tshirt_image_field.text()
        if not user_image or not tshirt_image:
            QMessageBox.warning(self, "Error", "Please select both user image and t-shirt image")
            return

        result_folder = "Results"  # Specify result folder
        try:
            result_image = process_image(user_image, tshirt_image, result_folder)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def stop_processing(self):
        QMessageBox.information(self, "Processing", "Processing stopped")


# Window for Try-On with Video
class TryWithVideoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Try-On with Video")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()

        # Field for selecting video
        self.video_label = QLabel("Select Your Video:")
        self.video_field = QLineEdit()
        self.video_button = QPushButton("Browse")
        self.video_button.clicked.connect(self.select_video)
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.video_field)
        self.layout.addWidget(self.video_button)

        # Field for selecting t-shirt image
        self.tshirt_image_label = QLabel("Select Your T-shirt Image:")
        self.tshirt_image_field = QLineEdit()
        self.tshirt_image_button = QPushButton("Browse")
        self.tshirt_image_button.clicked.connect(self.select_tshirt_image)
        self.layout.addWidget(self.tshirt_image_label)
        self.layout.addWidget(self.tshirt_image_field)
        self.layout.addWidget(self.tshirt_image_button)

        # Buttons for processing
        self.process_button = QPushButton("Start Processing")
        self.process_button.clicked.connect(self.start_processing)
        self.stop_button = QPushButton("Stop Processing")
        self.stop_button.clicked.connect(self.stop_processing)
        self.layout.addWidget(self.process_button)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)
        # Apply CSS styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: 'Helvetica Neue', sans-serif;
                font-size: 14px;
            }
            
            QLabel {
                color: #444444;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
                margin-bottom: 12px;
            }

            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                margin-bottom: 15px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #004085;
            }

            QPushButton:disabled {
                background-color: #e0e0e0;
                cursor: not-allowed;
            }

            QLineEdit:focus {
                border-color: #66afe9;
                outline: none;
            }
        """)

    def select_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi)")
        if file_name:
            self.video_field.setText(file_name)

    def select_tshirt_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select T-shirt Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.tshirt_image_field.setText(file_name)

    def start_processing(self):
        video_file = self.video_field.text()
        tshirt_image = self.tshirt_image_field.text()
        if not video_file or not tshirt_image:
            QMessageBox.warning(self, "Error", "Please select both video and t-shirt image")
            return

        result_folder = "Results"  # Specify result folder
        try:
            process_video_or_realtime(video_file, tshirt_image, result_folder)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def stop_processing(self):
        QMessageBox.information(self, "Processing", "Processing stopped")


# Window for Try-On with Real-time Video Capture
class TryWithRealtimeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Try-On with Real-time Video Capture")
        self.setGeometry(150, 150, 600, 400)
        self.layout = QVBoxLayout()

        # Field for selecting t-shirt image
        self.tshirt_image_label = QLabel("Select Your T-shirt Image:")
        self.tshirt_image_field = QLineEdit()
        self.tshirt_image_button = QPushButton("Browse")
        self.tshirt_image_button.clicked.connect(self.select_tshirt_image)
        self.layout.addWidget(self.tshirt_image_label)
        self.layout.addWidget(self.tshirt_image_field)
        self.layout.addWidget(self.tshirt_image_button)

        # Buttons for processing
        self.process_button = QPushButton("Start Real-time Capture")
        self.process_button.clicked.connect(self.start_processing)
        self.stop_button = QPushButton("Stop Capture")
        self.stop_button.clicked.connect(self.stop_processing)
        self.layout.addWidget(self.process_button)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)
        # Apply CSS styling
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QLabel {
                color: #2c3e50;
                font-weight: bold;
                margin-bottom: 8px;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ecf0f1;
                margin-bottom: 12px;
                font-size: 14px;
            }

            QPushButton {
                padding: 12px 25px;
                font-size: 14px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 15px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QPushButton:pressed {
                background-color: #1f6b8c;
            }

            QPushButton:disabled {
                background-color: #bdc3c7;
                cursor: not-allowed;
            }

            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)

    def select_tshirt_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select T-shirt Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.tshirt_image_field.setText(file_name)

    def start_processing(self):
        tshirt_image = self.tshirt_image_field.text()
        if not tshirt_image:
            QMessageBox.warning(self, "Error", "Please select t-shirt image")
            return

        result_folder = "Results"  # Specify result folder
        try:
            process_video_or_realtime(0, tshirt_image, result_folder)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def stop_processing(self):
        QMessageBox.information(self, "Processing", "Processing stopped")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
