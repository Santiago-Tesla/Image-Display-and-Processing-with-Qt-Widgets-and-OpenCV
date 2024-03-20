import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QSlider, QAction, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class VideoProcessor(QWidget):
    """
    Class responsible for handling video processing tasks.

    Emits a signal `frame_update_signal` whenever a new frame is processed.
    """

    frame_update_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.processing_enabled = False
        self.edge_detection_enabled = False   
        self.gray_threshold_enabled = False   
        self.face_detection_enabled = False   
        self.eye_detection_enabled = False   
        self.threshold = 127

    def start_camera(self, camera_id=0):
        """
        Starts video capture from the specified camera ID (defaults to 0).

        Emits the `frame_update_signal` whenever a new frame is captured.
        """
        self.cap = cv2.VideoCapture(camera_id)
        self.timer.start(30)  # Update every 30 milliseconds
        self.processing_enabled = False

    def stop_camera(self):
        #Stops video capture and releases resources
        self.timer.stop()
        if self.cap:
            self.cap.release()

    def update_frame(self):
        """
        Captures a frame from the camera, performs image processing if enabled,
        and emits the `frame_update_signal` with the processed frame.
        """
        ret, frame = self.cap.read()
        if ret:
            if self.processing_enabled:
                frame = self.process_frame(frame)
            self.frame_update_signal.emit(frame)

    def process_frame(self, frame):
        """
        Applies image processing based on enabled options.

        - Edge detection using Canny edge detection
        - Grayscale thresholding
        - Face detection using Haar cascade classifier
        - Eye detection using Haar cascade classifier

        Returns the processed frame.
        """
        if self.edge_detection_enabled:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.Canny(frame, 100, 200)  # Canny edge detection
        elif self.gray_threshold_enabled:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            _, thresholded_frame = cv2.threshold(gray_frame, self.threshold, 255, cv2.THRESH_BINARY)
            frame = cv2.cvtColor(thresholded_frame, cv2.COLOR_GRAY2BGR)
        elif self.face_detection_enabled:
            # Face detection using Haar cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        elif self.eye_detection_enabled:
            # Eye detection using Haar cascade classifier
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in eyes:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return frame


class MainWindow(QMainWindow):
    """
    Main window class for the video processing application.

    Connects signals and slots for various functionalities and displays the video stream.
    """
    def __init__(self):
        super().__init__()
        self.video_processor = VideoProcessor()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.start_camera)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        layout.addWidget(self.stop_button)

        self.options_layout = QHBoxLayout()
        layout.addLayout(self.options_layout)

        self.edge_detection_button = QPushButton("Edge Detection")
        self.edge_detection_button.clicked.connect(self.enable_edge_detection)
        self.options_layout.addWidget(self.edge_detection_button)

        self.gray_threshold_button = QPushButton("Grayscale with Threshold")
        self.gray_threshold_button.clicked.connect(self.enable_gray_threshold)
        self.options_layout.addWidget(self.gray_threshold_button)

        self.face_detection_button = QPushButton("Face Detection")
        self.face_detection_button.clicked.connect(self.enable_face_detection)
        self.options_layout.addWidget(self.face_detection_button)

        self.eye_detection_button = QPushButton("Eye Detection")
        self.eye_detection_button.clicked.connect(self.enable_eye_detection)
        self.options_layout.addWidget(self.eye_detection_button)

        self.save_frame_button = QPushButton("Save Frame")
        self.save_frame_button.clicked.connect(self.save_frame)
        self.options_layout.addWidget(self.save_frame_button)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(127)
        self.threshold_slider.setTickInterval(1)
        self.threshold_slider.valueChanged.connect(self.set_threshold)
        layout.addWidget(self.threshold_slider)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(QApplication.quit)  # Connect to quit the application
        layout.addWidget(self.exit_button)

        self.video_processor.frame_update_signal.connect(self.update_label)

    def start_camera(self):
        self.video_processor.start_camera()

    def stop_camera(self):
        self.video_processor.stop_camera()

    def update_label(self, frame):
        """
        Updates the displayed frame on the label based on the received frame.

        Performs BGR to RGB conversion for proper display in Qt.
        """
        if self.video_processor.edge_detection_enabled:
            # Converting single channel grayscale to 3-channel BGR for QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        else:
            # Converting BGR to RGB for QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytesPerLine = ch * w
        image = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)


    def enable_edge_detection(self):
        #Enables edge detection processing and disables other options
        self.video_processor.processing_enabled = True
        self.video_processor.edge_detection_enabled = True
        self.video_processor.gray_threshold_enabled = False
        self.video_processor.face_detection_enabled = False
        self.video_processor.eye_detection_enabled = False

    def enable_gray_threshold(self):
        #Enables grayscale thresholding processing and disables other options
        self.video_processor.processing_enabled = True
        self.video_processor.edge_detection_enabled = False
        self.video_processor.gray_threshold_enabled = True
        self.video_processor.face_detection_enabled = False
        self.video_processor.eye_detection_enabled = False

    def enable_face_detection(self):
        #Enables face detection processing and disables other options
        self.video_processor.processing_enabled = True
        self.video_processor.edge_detection_enabled = False
        self.video_processor.gray_threshold_enabled = False
        self.video_processor.face_detection_enabled = True
        self.video_processor.eye_detection_enabled = False

    def enable_eye_detection(self):
        #Enables eye detection processing and disables other options
        self.video_processor.processing_enabled = True
        self.video_processor.edge_detection_enabled = False
        self.video_processor.gray_threshold_enabled = False
        self.video_processor.face_detection_enabled = False
        self.video_processor.eye_detection_enabled = True

    def set_threshold(self, value):
        #Sets the threshold value for grayscale thresholding
        self.video_processor.threshold = value

    def save_frame(self):
        #Saves the current frame to an image file
        if not self.label.pixmap():
            QMessageBox.warning(self, "Error", "No frame to save.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save Frame", "", "Images (*.png *.jpg *.bmp)")
        if filename:
            self.label.pixmap().save(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
