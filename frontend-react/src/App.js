import React, { useState } from 'react';
import { Mail, User, Briefcase, MapPin, FileText, Send, Loader2, Upload, X } from 'lucide-react';

const API = 'http://127.0.0.1:8000';

// Header Component
const Header = () => (
  <div className="header">
    <div className="header-content">
      <Mail size={40} />
      <h1>AI Cold Email Generator</h1>
    </div>
    <p>Create personalized cold emails powered by AI</p>
  </div>
);

// Input Field Component
const InputField = ({ label, icon: Icon, ...props }) => (
  <div className="input-group">
    <label>
      {Icon && <Icon size={16} />}
      {label}
    </label>
    <input {...props} />
  </div>
);

// Textarea Component
const TextAreaField = ({ label, icon: Icon, ...props }) => (
  <div className="input-group">
    <label>
      {Icon && <Icon size={16} />}
      {label}
    </label>
    <textarea {...props} />
  </div>
);

// Section Title Component
const SectionTitle = ({ icon: Icon, children }) => (
  <div className="section-title">
    <div className="section-bar"></div>
    {Icon && <Icon size={24} />}
    <span>{children}</span>
  </div>
);

// File Upload Component
const FileUpload = ({ selectedFile, onFileSelect, onFileRemove }) => {
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type === 'application/pdf') {
        onFileSelect(file);
      } else {
        alert('Please select a PDF file only');
        e.target.value = '';
      }
    }
  };

  return (
    <div className="input-group">
      <label>
        <Upload size={16} />
        Attach PDF Resume (Optional)
      </label>
      <div className="file-wrapper">
        <input
          type="file"
          id="pdfAttachment"
          accept=".pdf"
          onChange={handleChange}
          className="file-input"
        />
        <label htmlFor="pdfAttachment" className="file-label">
          <Upload size={20} />
          <span>Choose PDF File</span>
        </label>
      </div>
      {selectedFile && (
        <div className="file-selected">
          <FileText size={16} />
          <span>{selectedFile.name}</span>
          <button type="button" onClick={onFileRemove} className="remove-btn">
            <X size={14} />
          </button>
        </div>
      )}
    </div>
  );
};

// Loading Component
const LoadingSpinner = () => (
  <div className="loading">
    <div className="spinner">
      <Loader2 className="spinner-icon" size={40} />
    </div>
    <p>Generating your personalized email...</p>
  </div>
);

// Main App Component
const App = () => {
  const [formData, setFormData] = useState({
    candidate_name: '',
    recipient_email: '',
    recipient_name: '',
    recipient_position: '',
    company_name: '',
    company_location: '',
    resume_text: ''
  });

  const [emailId, setEmailId] = useState(null);
  const [emailBody, setEmailBody] = useState('');
  const [subject, setSubject] = useState('Application for Software Engineer');
  const [selectedPdf, setSelectedPdf] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [sending, setSending] = useState(false);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = error => reject(error);
    });
  };

  const handleGenerateEmail = async (e) => {
    e.preventDefault();
    setLoading(true);
    setShowPreview(false);

    try {
      const response = await fetch(`${API}/generate-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      setEmailBody(data.email_body);
      setEmailId(data.email_id);
      setLoading(false);
      setShowPreview(true);

      setTimeout(() => {
        document.getElementById('preview')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (error) {
      setLoading(false);
      alert('Error generating email: ' + error.message);
    }
  };

  const handleSendEmail = async () => {
    setSending(true);

    try {
      const payload = {
        email_id: emailId,
        to_email: formData.recipient_email,
        subject: subject,
        edited_body: emailBody
      };

      if (selectedPdf) {
        const base64Content = await fileToBase64(selectedPdf);
        payload.attachment_filename = selectedPdf.name;
        payload.attachment_content = base64Content;
      }

      await fetch(`${API}/send-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      alert('✅ Email sent successfully!');
      setSelectedPdf(null);
    } catch (error) {
      alert('Error sending email: ' + error.message);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="app-container">
      <div className="container">
        <Header />

        <div className="content">
          <div>
            <div className="form-section">
              <SectionTitle icon={User}>Your Information</SectionTitle>
              <InputField
                label="Your Name"
                icon={User}
                name="candidate_name"
                type="text"
                placeholder="John Doe"
                value={formData.candidate_name}
                onChange={handleInputChange}
                required
              />
              <TextAreaField
                label="Your Resume"
                icon={FileText}
                name="resume_text"
                placeholder="Paste your resume or key qualifications here..."
                rows={6}
                value={formData.resume_text}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-section">
              <SectionTitle icon={Briefcase}>Recipient Details</SectionTitle>
              <div className="grid">
                <InputField
                  label="Recipient Name"
                  icon={User}
                  name="recipient_name"
                  type="text"
                  placeholder="Jane Smith"
                  value={formData.recipient_name}
                  onChange={handleInputChange}
                  required
                />
                <InputField
                  label="Recipient Email"
                  icon={Mail}
                  name="recipient_email"
                  type="email"
                  placeholder="jane@company.com"
                  value={formData.recipient_email}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="grid">
                <InputField
                  label="Position"
                  icon={Briefcase}
                  name="recipient_position"
                  type="text"
                  placeholder="Hiring Manager"
                  value={formData.recipient_position}
                  onChange={handleInputChange}
                  required
                />
                <InputField
                  label="Company Name"
                  icon={Briefcase}
                  name="company_name"
                  type="text"
                  placeholder="Tech Corp"
                  value={formData.company_name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <InputField
                label="Company Location"
                icon={MapPin}
                name="company_location"
                type="text"
                placeholder="San Francisco, CA"
                value={formData.company_location}
                onChange={handleInputChange}
                required
              />
            </div>

            <button onClick={handleGenerateEmail} type="button" className="btn btn-primary">
              <Mail size={20} />
              Generate Email
            </button>
          </div>

          {loading && <LoadingSpinner />}

          {showPreview && (
            <div id="preview" className="preview">
              <h2>
                <Mail size={28} />
                Your Generated Email
              </h2>

              <InputField
                label="Email Subject"
                icon={Mail}
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />

              <TextAreaField
                label="Email Body"
                icon={FileText}
                rows={12}
                value={emailBody}
                onChange={(e) => setEmailBody(e.target.value)}
              />

              <FileUpload
                selectedFile={selectedPdf}
                onFileSelect={setSelectedPdf}
                onFileRemove={() => setSelectedPdf(null)}
              />

              <button
                onClick={handleSendEmail}
                disabled={sending}
                className="btn btn-send"
              >
                {sending ? (
                  <>
                    <Loader2 className="spinner-icon" size={20} />
                    Sending...
                  </>
                ) : (
                  <>
                    <Send size={20} />
                    Send Email
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>

      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        .app-container {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }

        .container {
          max-width: 900px;
          margin: 0 auto;
          background: white;
          border-radius: 24px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
          overflow: hidden;
        }

        .header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 50px 40px;
          text-align: center;
          color: white;
        }

        .header-content {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 15px;
          margin-bottom: 10px;
        }

        .header h1 {
          font-size: 2.5rem;
          font-weight: 600;
          margin: 0;
        }

        .header p {
          font-size: 1.1rem;
          opacity: 0.95;
          margin: 0;
        }

        .content {
          padding: 40px;
        }

        .form-section {
          margin-bottom: 40px;
        }

        .section-title {
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 1.4rem;
          color: #667eea;
          margin-bottom: 25px;
          font-weight: 600;
        }

        .section-bar {
          width: 4px;
          height: 28px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 2px;
        }

        .input-group {
          margin-bottom: 20px;
        }

        .input-group label {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 10px;
          color: #4a5568;
          font-weight: 500;
          font-size: 0.95rem;
        }

        .input-group label svg {
          color: #667eea;
        }

        .input-group input,
        .input-group textarea {
          width: 100%;
          padding: 14px 18px;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          font-size: 1rem;
          font-family: inherit;
          background: #f7fafc;
          transition: all 0.3s ease;
        }

        .input-group input:focus,
        .input-group textarea:focus {
          outline: none;
          border-color: #667eea;
          background: white;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .input-group textarea {
          resize: vertical;
          min-height: 120px;
          line-height: 1.6;
        }

        .grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          margin-bottom: 20px;
        }

        .btn {
          width: 100%;
          padding: 16px 24px;
          border: none;
          border-radius: 12px;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
        }

        .btn-primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        .btn-primary:active {
          transform: translateY(0);
        }

        .btn-send {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        }

        .btn-send:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6);
        }

        .btn-send:disabled {
          background: #cbd5e0;
          cursor: not-allowed;
          transform: none;
          box-shadow: none;
        }

        .loading {
          text-align: center;
          padding: 40px 20px;
          animation: fadeIn 0.4s ease;
        }

        .spinner {
          margin: 0 auto 15px;
        }

        .spinner-icon {
          color: #667eea;
          animation: spin 1s linear infinite;
        }

        .loading p {
          color: #667eea;
          font-weight: 500;
          font-size: 1.1rem;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .preview {
          margin-top: 50px;
          padding: 35px;
          background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
          border-radius: 20px;
          animation: fadeIn 0.4s ease;
        }

        .preview h2 {
          display: flex;
          align-items: center;
          gap: 12px;
          color: #667eea;
          margin-bottom: 30px;
          font-size: 1.8rem;
          font-weight: 700;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .file-wrapper {
          position: relative;
        }

        .file-input {
          position: absolute;
          left: -9999px;
        }

        .file-label {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
          padding: 14px 18px;
          background: #f7fafc;
          border: 2px dashed #e2e8f0;
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.3s ease;
          color: #4a5568;
          font-weight: 500;
        }

        .file-label:hover {
          border-color: #667eea;
          background: white;
        }

        .file-selected {
          margin-top: 12px;
          display: inline-flex;
          align-items: center;
          gap: 10px;
          padding: 10px 16px;
          background: #667eea;
          color: white;
          border-radius: 10px;
          font-size: 0.95rem;
        }

        .remove-btn {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          color: white;
          padding: 4px 10px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.85rem;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .remove-btn:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        @media (max-width: 768px) {
          .grid {
            grid-template-columns: 1fr;
          }

          .header h1 {
            font-size: 2rem;
          }

          .content {
            padding: 30px 20px;
          }

          .header {
            padding: 40px 20px;
          }

          .preview {
            padding: 25px;
          }
        }
      `}</style>
    </div>
  );
};

export default App;