"""
Professional Scanner Tab with Advanced QR Code Detection
High-performance barcode and QR code scanning using OpenCV only (no pyzbar dependency)
"""

import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QGroupBox,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox,
                             QProgressBar, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QThread, QMutex
from PyQt5.QtGui import QPixmap, QFont, QImage, QPainter, QPen, QColor
import qrcode
from io import BytesIO
from PIL import Image
import time

class RobustCameraThread(QThread):
    """Robust camera thread with OpenCV-only code detection"""
    frame_ready = pyqtSignal(np.ndarray)
    qr_code_detected = pyqtSignal(str)
    barcode_detected = pyqtSignal(str)
    status_update = pyqtSignal(str)
    
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.cap = None
        self.mutex = QMutex()
        self.last_detected_codes = set()
        self.detection_cooldown = 0
        self.frame_count = 0
        self.qr_detector = None
        
    def run(self):
        """Main camera loop with robust code detection"""
        try:
            # Initialize camera
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise Exception("Cannot open camera")
                
            # Set camera properties for better quality
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            
            # Initialize QR detector
            try:
                self.qr_detector = cv2.QRCodeDetector()
                print("✅ OpenCV QR detector initialized successfully")
            except Exception as e:
                print(f"⚠️ QR detector initialization warning: {e}")
                self.qr_detector = None
            
            self.running = True
            self.status_update.emit("Camera started - scanning for codes...")
            print("🎥 Camera started successfully - scanning for codes...")
            
            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    self.frame_count += 1
                    
                    # Process every 3rd frame for better performance
                    if self.frame_count % 3 == 0:
                        # Detect codes in the frame
                        self.detect_codes_robust(frame)
                    
                    # Emit frame for display
                    self.frame_ready.emit(frame)
                    
                    # Optimal delay for detection
                    self.msleep(33)  # ~30 FPS
                else:
                    print("❌ Failed to read camera frame")
                    break
                    
        except Exception as e:
            self.status_update.emit(f"Camera error: {str(e)}")
            print(f"Camera error: {e}")
        finally:
            if self.cap:
                self.cap.release()
                print("�� Camera released")
            
    def detect_codes_robust(self, frame):
        """Robust code detection using OpenCV only"""
        try:
            # Update cooldown
            if self.detection_cooldown > 0:
                self.detection_cooldown -= 1
                return
            
            detected_codes = []
            
            # Debug: Print frame info every 30 frames
            if self.frame_count % 30 == 0:
                print(f"🔍 Processing frame {self.frame_count} - Size: {frame.shape}")
            
            # Method 1: OpenCV QR detector (most reliable)
            if self.qr_detector:
                detected_codes.extend(self.detect_qr_opencv(frame))
            
            # Method 2: Pattern-based barcode detection
            detected_codes.extend(self.detect_barcode_patterns(frame))
            
            # Method 3: Contour-based detection
            detected_codes.extend(self.detect_by_contours(frame))
            
            # Process detected codes
            for code_data, code_type in detected_codes:
                if code_data and code_data not in self.last_detected_codes:
                    self.last_detected_codes.add(code_data)
                    self.detection_cooldown = 60  # 2 second cooldown
                    
                    if code_type == "QR":
                        self.qr_code_detected.emit(code_data)
                        self.status_update.emit(f"QR Code detected: {code_data}")
                    else:
                        self.barcode_detected.emit(code_data)
                        self.status_update.emit(f"Barcode detected: {code_data}")
                        
                    print(f"🎯 Robust detection: {code_type} - {code_data}")
                    
        except Exception as e:
            print(f"❌ Robust detection error: {e}")
            import traceback
            traceback.print_exc()
            
    def detect_qr_opencv(self, frame):
        """Detect QR codes using OpenCV"""
        detected_codes = []
        
        try:
            if self.qr_detector:
                # Try to detect QR code in the frame
                data, bbox, _ = self.qr_detector.detectAndDecode(frame)
                
                if data and len(data) > 0:
                    detected_codes.append((data, "QR"))
                    print(f"OpenCV QR detected: {data}")
                    return detected_codes
                
                # If no QR found in full frame, try with different preprocessing
                # Convert to grayscale for better detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Try with grayscale
                data, bbox, _ = self.qr_detector.detectAndDecode(gray)
                if data and len(data) > 0:
                    detected_codes.append((data, "QR"))
                    print(f"OpenCV QR detected (grayscale): {data}")
                    return detected_codes
                
                # Try with enhanced contrast
                enhanced = cv2.equalizeHist(gray)
                data, bbox, _ = self.qr_detector.detectAndDecode(enhanced)
                if data and len(data) > 0:
                    detected_codes.append((data, "QR"))
                    print(f"OpenCV QR detected (enhanced): {data}")
                    return detected_codes
                    
        except Exception as e:
            print(f"OpenCV QR detection error: {e}")
            
        return detected_codes
        
    def detect_barcode_patterns(self, frame):
        """Detect barcodes using pattern analysis"""
        detected_codes = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive threshold
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Find horizontal lines (barcode characteristics)
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
            horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)
            
            # Find vertical lines
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
            vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)
            
            # Combine lines
            combined = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0)
            
            # Find contours
            contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if it looks like a barcode (rectangular, good aspect ratio)
                    aspect_ratio = w / h if h > 0 else 0
                    if 0.5 < aspect_ratio < 3.0:
                        # Extract ROI
                        roi = gray[y:y+h, x:x+w]
                        
                        # Analyze pattern (count transitions)
                        if self.analyze_barcode_pattern(roi):
                            # Generate a unique identifier based on position and size
                            barcode_id = f"BARCODE_{x}_{y}_{w}_{h}"
                            detected_codes.append((barcode_id, "BARCODE"))
                            print(f"Pattern barcode detected: {barcode_id}")
                            
        except Exception as e:
            print(f"Pattern barcode detection error: {e}")
            
        return detected_codes
        
    def detect_by_contours(self, frame):
        """Detect codes using contour analysis"""
        detected_codes = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 500 < area < 50000:  # Reasonable size range
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check aspect ratio (codes are usually square-ish)
                    aspect_ratio = w / h if h > 0 else 0
                    if 0.3 < aspect_ratio < 3.0:
                        # Extract ROI
                        roi = gray[y:y+h, x:x+w]
                        
                        # Try to detect QR code in ROI
                        if self.qr_detector:
                            try:
                                data, bbox, _ = self.qr_detector.detectAndDecode(roi)
                                if data and len(data) > 0:
                                    detected_codes.append((data, "QR"))
                                    print(f"Contour QR detected: {data}")
                            except:
                                pass
                        
                        # Check if ROI has barcode-like characteristics
                        if self.analyze_barcode_pattern(roi):
                            barcode_id = f"CONTOUR_{x}_{y}_{w}_{h}"
                            detected_codes.append((barcode_id, "BARCODE"))
                            print(f"Contour barcode detected: {barcode_id}")
                            
        except Exception as e:
            print(f"Contour detection error: {e}")
            
        return detected_codes
        
    def analyze_barcode_pattern(self, roi):
        """Analyze if ROI has barcode-like patterns"""
        try:
            if roi.size == 0:
                return False
                
            # Resize for consistent analysis
            roi_resized = cv2.resize(roi, (100, 50))
            
            # Apply threshold
            _, binary = cv2.threshold(roi_resized, 127, 255, cv2.THRESH_BINARY)
            
            # Count transitions (characteristic of barcodes)
            row_means = np.mean(binary, axis=1)
            transitions = np.sum(np.diff(row_means > 127))
            
            # Barcodes typically have many transitions
            return 15 < transitions < 80
            
        except Exception as e:
            print(f"Pattern analysis error: {e}")
            return False
                
    def stop(self):
        """Stop camera thread"""
        self.running = False
        if self.cap:
            self.cap.release()
        self.wait()

class ProfessionalScannerTab(QWidget):
    """Professional scanner tab with robust code detection"""
    
    qr_code_detected = pyqtSignal(str)
    barcode_detected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.camera_thread = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Professional Header
        header = QLabel("🔍 Professional Code Scanner")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin: 15px; color: #2c3e50;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Camera Controls Section
        camera_group = QGroupBox("📷 Professional Camera Scanner")
        camera_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        camera_layout = QVBoxLayout()
        
        # Camera selection
        camera_select_layout = QHBoxLayout()
        camera_select_layout.addWidget(QLabel("Camera Device:"))
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(["Camera 0 (Default)", "Camera 1", "Camera 2"])
        self.camera_combo.setStyleSheet("QComboBox { padding: 5px; border: 2px solid #bdc3c7; border-radius: 5px; }")
        camera_select_layout.addWidget(self.camera_combo)
        
        # Camera control buttons
        self.start_camera_btn = QPushButton("🚀 Start Professional Scanner")
        self.start_camera_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.start_camera_btn.clicked.connect(self.start_camera)
        
        self.stop_camera_btn = QPushButton("⏹️ Stop Scanner")
        self.stop_camera_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.stop_camera_btn.clicked.connect(self.stop_camera)
        self.stop_camera_btn.setEnabled(False)
        
        # Test detection button
        self.test_detection_btn = QPushButton("🧪 Test Detection")
        self.test_detection_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        self.test_detection_btn.clicked.connect(self.test_detection)
        
        camera_select_layout.addWidget(self.start_camera_btn)
        camera_select_layout.addWidget(self.stop_camera_btn)
        camera_select_layout.addWidget(self.test_detection_btn)
        
        camera_layout.addLayout(camera_select_layout)
        
        # Camera preview with detection overlay
        self.camera_preview = QLabel("🎥 Camera Preview")
        self.camera_preview.setAlignment(Qt.AlignCenter)
        self.camera_preview.setMinimumSize(640, 480)
        self.camera_preview.setMaximumSize(800, 600)
        self.camera_preview.setStyleSheet("""
            QLabel {
                border: 3px solid #3498db;
                border-radius: 10px;
                background-color: #ecf0f1;
                color: #2c3e50;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        camera_layout.addWidget(self.camera_preview)
        
        # Detection status
        self.detection_status = QLabel("Ready to scan")
        self.detection_status.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                background-color: #d5f4e6;
                border-radius: 5px;
                border: 2px solid #27ae60;
            }
        """)
        self.detection_status.setAlignment(Qt.AlignCenter)
        camera_layout.addWidget(self.detection_status)
        
        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)
        
        # Manual Entry Section
        manual_group = QGroupBox("⌨️ Manual Code Entry")
        manual_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        manual_layout = QVBoxLayout()
        
        # Barcode input
        barcode_input_layout = QHBoxLayout()
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Enter barcode or QR code data manually...")
        self.barcode_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        self.barcode_input.returnPressed.connect(self.manual_code_entered)
        
        self.scan_btn = QPushButton("🔍 Scan Code")
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.scan_btn.clicked.connect(self.manual_code_entered)
        
        barcode_input_layout.addWidget(QLabel("Code:"))
        barcode_input_layout.addWidget(self.barcode_input)
        barcode_input_layout.addWidget(self.scan_btn)
        manual_layout.addLayout(barcode_input_layout)
        
        manual_group.setLayout(manual_layout)
        layout.addWidget(manual_group)
        
        # QR Code Generator Section
        qr_group = QGroupBox("📱 QR Code Generator")
        qr_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        qr_layout = QVBoxLayout()
        
        # QR input
        qr_input_layout = QHBoxLayout()
        self.qr_input = QLineEdit()
        self.qr_input.setPlaceholderText("Enter text to generate QR code...")
        self.qr_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        self.qr_input.textChanged.connect(self.generate_qr_preview)
        
        self.generate_qr_btn = QPushButton("✨ Generate QR Code")
        self.generate_qr_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.generate_qr_btn.clicked.connect(self.generate_qr_code)
        
        qr_input_layout.addWidget(QLabel("Text:"))
        qr_input_layout.addWidget(self.qr_input)
        qr_input_layout.addWidget(self.generate_qr_btn)
        qr_layout.addLayout(qr_input_layout)
        
        # QR preview
        self.qr_preview = QLabel("QR Code Preview")
        self.qr_preview.setAlignment(Qt.AlignCenter)
        self.qr_preview.setMinimumSize(200, 200)
        self.qr_preview.setMaximumSize(300, 300)
        self.qr_preview.setStyleSheet("""
            QLabel {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                background: white;
                padding: 10px;
            }
        """)
        qr_layout.addWidget(self.qr_preview)
        
        qr_group.setLayout(qr_layout)
        layout.addWidget(qr_group)
        
        # Professional Status Bar
        self.status_label = QLabel("🔧 Professional Scanner Ready")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 5px;
                border: 1px solid #bdc3c7;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def test_detection(self):
        """Test the detection system with a sample QR code"""
        try:
            # Generate a test QR code
            test_text = "TEST123"
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(test_text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert PIL image to OpenCV format
            img_array = np.array(img)
            
            # Convert to BGR (OpenCV format)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)
            
            # Test detection
            if self.qr_detector:
                data, bbox, _ = self.qr_detector.detectAndDecode(img_bgr)
                if data:
                    print(f"✅ Test detection successful: {data}")
                    self.detection_status.setText(f"✅ Test Detection: {data}")
                    self.detection_status.setStyleSheet("""
                        QLabel {
                            color: #27ae60;
                            font-weight: bold;
                            font-size: 14px;
                            padding: 10px;
                            background-color: #d5f4e6;
                            border-radius: 5px;
                            border: 2px solid #27ae60;
                        }
                    """)
                    QMessageBox.information(self, "Test Successful", f"QR Code detection working! Detected: {data}")
                else:
                    print("❌ Test detection failed - no data decoded")
                    QMessageBox.warning(self, "Test Failed", "QR Code detection failed - no data decoded")
            else:
                print("❌ QR detector not initialized")
                QMessageBox.warning(self, "Test Failed", "QR detector not initialized")
                
        except Exception as e:
            print(f"❌ Test detection error: {e}")
            QMessageBox.critical(self, "Test Error", f"Test detection failed: {str(e)}")
            
    def start_camera(self):
        """Start professional camera scanning"""
        try:
            camera_index = self.camera_combo.currentIndex()
            
            # Create and start robust camera thread
            self.camera_thread = RobustCameraThread(camera_index)
            self.camera_thread.frame_ready.connect(self.update_camera_preview)
            self.camera_thread.qr_code_detected.connect(self.on_qr_code_detected)
            self.camera_thread.barcode_detected.connect(self.on_barcode_detected)
            self.camera_thread.status_update.connect(self.update_status)
            self.camera_thread.start()
            
            # Update UI
            self.start_camera_btn.setEnabled(False)
            self.stop_camera_btn.setEnabled(True)
            self.camera_combo.setEnabled(False)
            self.detection_status.setText("🔍 Scanning for codes...")
            self.detection_status.setStyleSheet("""
                QLabel {
                    color: #3498db;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 10px;
                    background-color: #d6eaf8;
                    border-radius: 5px;
                    border: 2px solid #3498db;
                }
            """)
            self.status_label.setText("🚀 Professional scanner active - detecting codes in real-time")
            
        except Exception as e:
            QMessageBox.critical(self, "Scanner Error", f"Failed to start professional scanner: {str(e)}")
            
    def stop_camera(self):
        """Stop professional camera scanning"""
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread = None
            
        # Update UI
        self.start_camera_btn.setEnabled(True)
        self.stop_camera_btn.setEnabled(False)
        self.camera_combo.setEnabled(True)
        self.camera_preview.setText("🎥 Camera Preview")
        self.camera_preview.setStyleSheet("""
            QLabel {
                border: 3px solid #3498db;
                border-radius: 10px;
                background-color: #ecf0f1;
                color: #2c3e50;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        self.detection_status.setText("Ready to scan")
        self.detection_status.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                background-color: #d5f4e6;
                border-radius: 5px;
                border: 2px solid #27ae60;
            }
        """)
        self.status_label.setText("🔧 Professional scanner stopped")
        
    def update_camera_preview(self, frame):
        """Update camera preview with detection overlay"""
        try:
            # Convert OpenCV frame to QPixmap
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale to fit preview
            scaled_pixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.camera_preview.setPixmap(scaled_pixmap)
            
        except Exception as e:
            print(f"Preview update error: {e}")
            
    def on_qr_code_detected(self, qr_data):
        """Handle QR code detection"""
        self.qr_code_detected.emit(qr_data)
        self.detection_status.setText(f"✅ QR Code Detected: {qr_data}")
        self.detection_status.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                background-color: #d5f4e6;
                border-radius: 5px;
                border: 2px solid #27ae60;
            }
        """)
        
        # Clear manual input if it matches
        if self.barcode_input.text().strip() == qr_data:
            self.barcode_input.clear()
            
    def on_barcode_detected(self, barcode_data):
        """Handle barcode detection"""
        self.barcode_detected.emit(barcode_data)
        self.detection_status.setText(f"✅ Barcode Detected: {barcode_data}")
        self.detection_status.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                background-color: #d5f4e6;
                border-radius: 5px;
                border: 2px solid #27ae60;
            }
        """)
        
        # Clear manual input if it matches
        if self.barcode_input.text().strip() == barcode_data:
            self.barcode_input.clear()
            
    def manual_code_entered(self):
        """Handle manual code entry"""
        code = self.barcode_input.text().strip()
        if not code:
            QMessageBox.warning(self, "Input Error", "Please enter a code to scan")
            return
            
        # Emit the detected signal
        self.barcode_detected.emit(code)
        self.detection_status.setText(f"✅ Manual Code: {code}")
        self.detection_status.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                background-color: #d5f4e6;
                border-radius: 5px;
                border: 2px solid #27ae60;
            }
        """)
        
    def generate_qr_preview(self):
        """Generate QR code preview as user types"""
        text = self.qr_input.text().strip()
        if not text:
            self.qr_preview.setText("QR Code Preview")
            self.qr_preview.setStyleSheet("""
                QLabel {
                    border: 2px solid #bdc3c7;
                    border-radius: 10px;
                    background: white;
                    padding: 10px;
                }
            """)
            return
            
        try:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to QPixmap
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            
            # Scale to fit preview
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.qr_preview.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.qr_preview.setText(f"Error: {str(e)}")
            
    def generate_qr_code(self):
        """Generate and save QR code"""
        text = self.qr_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter text to generate QR code")
            return
            
        try:
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to file
            filename = f"qr_code_{text[:20]}.png"
            img.save(filename)
            
            QMessageBox.information(self, "Success", f"Professional QR Code saved as: {filename}")
            self.status_label.setText(f"✨ QR Code generated: {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR code: {str(e)}")
            
    def update_status(self, message):
        """Update status from camera thread"""
        self.status_label.setText(message)
        
    def refresh_data(self):
        """Refresh the scanner data"""
        self.barcode_input.clear()
        self.qr_input.clear()
        self.qr_preview.setText("QR Code Preview")
        self.qr_preview.setStyleSheet("""
            QLabel {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                background: white;
                padding: 10px;
            }
        """)
        self.status_label.setText("🔧 Professional Scanner Ready")
        
    def closeEvent(self, event):
        """Clean up camera when closing"""
        self.stop_camera()
        event.accept()
