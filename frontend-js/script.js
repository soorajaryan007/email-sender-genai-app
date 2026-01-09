    const API = 'http://127.0.0.1:8000';
    let emailId = null;
    let selectedPdfFile = null;

    const form = document.getElementById('emailForm');
    const preview = document.getElementById('preview');
    const emailBodyField = document.getElementById('emailBody');
    const subjectField = document.getElementById('subject');
    const sendBtn = document.getElementById('sendBtn');
    const loading = document.getElementById('loading');
    const pdfInput = document.getElementById('pdfAttachment');
    const fileNameDisplay = document.getElementById('fileName');

    // Handle PDF file selection
    pdfInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        if (file.type === 'application/pdf') {
          selectedPdfFile = file;
          fileNameDisplay.innerHTML = `
            <span class="file-name">
              📄 ${file.name}
              <button type="button" class="remove-file" onclick="removePdf()">✕</button>
            </span>
          `;
          fileNameDisplay.style.display = 'block';
        } else {
          alert('Please select a PDF file only');
          pdfInput.value = '';
          selectedPdfFile = null;
        }
      }
    });

    // Remove PDF function
    window.removePdf = function() {
      selectedPdfFile = null;
      pdfInput.value = '';
      fileNameDisplay.style.display = 'none';
      fileNameDisplay.innerHTML = '';
    };

    // Convert file to base64
    function fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          // Remove the data:application/pdf;base64, prefix
          const base64String = reader.result.split(',')[1];
          resolve(base64String);
        };
        reader.onerror = error => reject(error);
      });
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = {
        candidate_name: document.getElementById('candidate_name').value,
        recipient_email: document.getElementById('recipient_email').value,
        recipient_name: document.getElementById('recipient_name').value,
        recipient_position: document.getElementById('recipient_position').value,
        company_name: document.getElementById('company_name').value,
        company_location: document.getElementById('company_location').value,
        resume_text: document.getElementById('resume_text').value
      };

      loading.classList.add('active');
      preview.classList.remove('visible');

      try {
        const response = await fetch(`${API}/generate-email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        emailBodyField.value = data.email_body;
        emailId = data.email_id;
        
        loading.classList.remove('active');
        preview.classList.add('visible');
        preview.scrollIntoView({ behavior: 'smooth' });
      } catch (error) {
        loading.classList.remove('active');
        alert('Error generating email: ' + error.message);
      }
    });

    sendBtn.addEventListener('click', async () => {
      const recipientEmail = document.getElementById('recipient_email').value;
      const subject = subjectField.value;
      const editedBody = emailBodyField.value;

      sendBtn.disabled = true;
      sendBtn.textContent = 'Sending...';

      try {
        const payload = {
          email_id: emailId,
          to_email: recipientEmail,
          subject: subject,
          edited_body: editedBody
        };

        // Add PDF attachment if selected
        if (selectedPdfFile) {
          const base64Content = await fileToBase64(selectedPdfFile);
          payload.attachment_filename = selectedPdfFile.name;
          payload.attachment_content = base64Content;
        }

        await fetch(`${API}/send-email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        alert('✅ Email sent successfully!');
        sendBtn.textContent = '✓ Sent';
        
        // Reset file input
        removePdf();
        
        setTimeout(() => {
          sendBtn.textContent = '🚀 Send Email';
          sendBtn.disabled = false;
        }, 2000);
      } catch (error) {
        alert('Error sending email: ' + error.message);
        sendBtn.textContent = '🚀 Send Email';
        sendBtn.disabled = false;
      }
    });