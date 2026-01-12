#!/usr/bin/env python3
"""
Cold Email Generator - Desktop Application
PyQt5 GUI for generating and sending professional cold emails
"""

import sys
import json
import base64
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QGroupBox,
    QFileDialog, QMessageBox, QProgressBar, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Import your existing modules
from app.llm import generate_cold_email
from app.store import save_email
from app.email_service import send_email


class EmailGeneratorThread(QThread):
    """Background thread for email generation"""
    finished = pyqtSignal(str, str)  # email_id, email_body
    error = pyqtSignal(str)
    
    def __init__(self, data):
        super().__init__()
        self.data = data
    
    def run(self):
        try:
            prompt = f"""
Candidate Resume: {self.data['resume_text']}
Candidate Name: {self.data['candidate_name']}

Recipient Details:
Name: {self.data['recipient_name']}
Position: {self.data['recipient_position']}
Company: {self.data['company_name']}
Location: {self.data['company_location']}
"""
            email_body = generate_cold_email(prompt)
            email_id = save_email(email_body)
            self.finished.emit(email_id, email_body)
        except Exception as e:
            self.error.emit(str(e))


class EmailSenderThread(QThread):
    """Background thread for sending emails"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, data):
        super().__init__()
        self.data = data
    
    def run(self):
        try:
            send_email(
                to_email=self.data['to_email'],
                subject=self.data['subject'],
                body=self.data['body'],
                attachment_filename=self.data.get('attachment_filename'),
                attachment_content=self.data.get('attachment_content')
            )
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class ColdEmailApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.email_id = None
        self.generated_email = None
        self.attachment_data = None
        self.attachment_filename = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Cold Email Generator")
        self.setGeometry(100, 100, 900, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Tab 1: Generate Email
        generate_tab = QWidget()
        generate_layout = QVBoxLayout(generate_tab)
        
        # Candidate Information Group
        candidate_group = QGroupBox("Candidate Information")
        candidate_layout = QVBoxLayout()
        
        self.candidate_name_input = self.create_input_field(
            candidate_layout, "Candidate Name:", "John Doe"
        )
        
        resume_label = QLabel("Resume/CV:")
        resume_label.setFont(QFont("Arial", 10, QFont.Bold))
        candidate_layout.addWidget(resume_label)
        
        self.resume_text = QTextEdit()
        self.resume_text.setPlaceholderText("Paste your resume or key qualifications here...")
        self.resume_text.setMaximumHeight(150)
        candidate_layout.addWidget(self.resume_text)
        
        # Resume file button
        resume_btn_layout = QHBoxLayout()
        self.load_resume_btn = QPushButton("📄 Load Resume from File")
        self.load_resume_btn.clicked.connect(self.load_resume_file)
        resume_btn_layout.addWidget(self.load_resume_btn)
        resume_btn_layout.addStretch()
        candidate_layout.addLayout(resume_btn_layout)
        
        candidate_group.setLayout(candidate_layout)
        generate_layout.addWidget(candidate_group)
        
        # Recipient Information Group
        recipient_group = QGroupBox("Recipient Information")
        recipient_layout = QVBoxLayout()
        
        self.recipient_name_input = self.create_input_field(
            recipient_layout, "Recipient Name:", "Jane Smith"
        )
        self.recipient_email_input = self.create_input_field(
            recipient_layout, "Recipient Email:", "jane.smith@company.com"
        )
        self.recipient_position_input = self.create_input_field(
            recipient_layout, "Position:", "Hiring Manager"
        )
        self.company_name_input = self.create_input_field(
            recipient_layout, "Company Name:", "Tech Corp"
        )
        self.company_location_input = self.create_input_field(
            recipient_layout, "Company Location:", "San Francisco, CA"
        )
        
        recipient_group.setLayout(recipient_layout)
        generate_layout.addWidget(recipient_group)
        
        # Generate Button
        self.generate_btn = QPushButton("✨ Generate Cold Email")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_email)
        generate_layout.addWidget(self.generate_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        generate_layout.addWidget(self.progress_bar)
        
        tabs.addTab(generate_tab, "📝 Generate Email")
        
        # Tab 2: Review & Send
        send_tab = QWidget()
        send_layout = QVBoxLayout(send_tab)
        
        # Email preview group
        preview_group = QGroupBox("Generated Email")
        preview_layout = QVBoxLayout()
        
        self.subject_input = self.create_input_field(
            preview_layout, "Subject:", "Application for [Position]"
        )
        
        body_label = QLabel("Email Body:")
        body_label.setFont(QFont("Arial", 10, QFont.Bold))
        preview_layout.addWidget(body_label)
        
        self.email_body_text = QTextEdit()
        self.email_body_text.setPlaceholderText("Generated email will appear here...")
        preview_layout.addWidget(self.email_body_text)
        
        preview_group.setLayout(preview_layout)
        send_layout.addWidget(preview_group)
        
        # Attachment section
        attachment_layout = QHBoxLayout()
        self.attach_btn = QPushButton("📎 Attach Resume (PDF)")
        self.attach_btn.clicked.connect(self.attach_file)
        attachment_layout.addWidget(self.attach_btn)
        
        self.attachment_label = QLabel("No file attached")
        attachment_layout.addWidget(self.attachment_label)
        attachment_layout.addStretch()
        send_layout.addLayout(attachment_layout)
        
        # Send button
        self.send_btn = QPushButton("📧 Send Email")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.send_btn.clicked.connect(self.send_email)
        send_layout.addWidget(self.send_btn)
        
        tabs.addTab(send_tab, "📨 Review & Send")
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_input_field(self, layout, label_text, placeholder):
        """Helper to create labeled input field"""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(label)
        
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        layout.addWidget(input_field)
        
        return input_field
    
    def load_resume_file(self):
        """Load resume from text file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Resume File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.resume_text.setPlainText(f.read())
                self.statusBar().showMessage(f"Loaded: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
    
    def attach_file(self):
        """Attach PDF resume"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Attach Resume", "", "PDF Files (*.pdf)"
        )
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    self.attachment_data = base64.b64encode(f.read()).decode('utf-8')
                    self.attachment_filename = Path(file_path).name
                    self.attachment_label.setText(f"✓ {self.attachment_filename}")
                    self.statusBar().showMessage(f"Attached: {self.attachment_filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to attach file: {str(e)}")
    
    def generate_email(self):
        """Generate cold email using LLM"""
        # Validate inputs
        if not self.candidate_name_input.text().strip():
            QMessageBox.warning(self, "Validation", "Please enter candidate name")
            return
        if not self.resume_text.toPlainText().strip():
            QMessageBox.warning(self, "Validation", "Please enter resume text")
            return
        if not self.recipient_name_input.text().strip():
            QMessageBox.warning(self, "Validation", "Please enter recipient name")
            return
        
        # Prepare data
        data = {
            'candidate_name': self.candidate_name_input.text(),
            'resume_text': self.resume_text.toPlainText(),
            'recipient_name': self.recipient_name_input.text(),
            'recipient_email': self.recipient_email_input.text(),
            'recipient_position': self.recipient_position_input.text(),
            'company_name': self.company_name_input.text(),
            'company_location': self.company_location_input.text()
        }
        
        # Disable button and show progress
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.statusBar().showMessage("Generating email...")
        
        # Start generation thread
        self.gen_thread = EmailGeneratorThread(data)
        self.gen_thread.finished.connect(self.on_email_generated)
        self.gen_thread.error.connect(self.on_generation_error)
        self.gen_thread.start()
    
    def on_email_generated(self, email_id, email_body):
        """Handle successful email generation"""
        self.email_id = email_id
        self.generated_email = email_body
        self.email_body_text.setPlainText(email_body)
        
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Email generated successfully!")
        
        QMessageBox.information(
            self, "Success", 
            "Email generated! Switch to 'Review & Send' tab to review and send."
        )
    
    def on_generation_error(self, error_msg):
        """Handle generation error"""
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Generation failed")
        QMessageBox.critical(self, "Error", f"Failed to generate email:\n{error_msg}")
    
    def send_email(self):
        """Send the generated email"""
        # Validate
        if not self.email_body_text.toPlainText().strip():
            QMessageBox.warning(self, "Validation", "No email to send. Generate one first.")
            return
        if not self.subject_input.text().strip():
            QMessageBox.warning(self, "Validation", "Please enter email subject")
            return
        if not self.recipient_email_input.text().strip():
            QMessageBox.warning(self, "Validation", "Please enter recipient email")
            return
        
        # Confirm
        reply = QMessageBox.question(
            self, "Confirm Send",
            f"Send email to {self.recipient_email_input.text()}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Prepare data
        data = {
            'to_email': self.recipient_email_input.text(),
            'subject': self.subject_input.text(),
            'body': self.email_body_text.toPlainText(),
            'attachment_filename': self.attachment_filename,
            'attachment_content': self.attachment_data
        }
        
        # Disable button
        self.send_btn.setEnabled(False)
        self.statusBar().showMessage("Sending email...")
        
        # Start send thread
        self.send_thread = EmailSenderThread(data)
        self.send_thread.finished.connect(self.on_email_sent)
        self.send_thread.error.connect(self.on_send_error)
        self.send_thread.start()
    
    def on_email_sent(self):
        """Handle successful email send"""
        self.send_btn.setEnabled(True)
        self.statusBar().showMessage("Email sent successfully!")
        QMessageBox.information(self, "Success", "Email sent successfully!")
    
    def on_send_error(self, error_msg):
        """Handle send error"""
        self.send_btn.setEnabled(True)
        self.statusBar().showMessage("Send failed")
        QMessageBox.critical(self, "Error", f"Failed to send email:\n{error_msg}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    window = ColdEmailApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()