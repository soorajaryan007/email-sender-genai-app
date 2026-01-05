    const API = 'http://127.0.0.1:8000';
    let emailId = null;

    const form = document.getElementById('emailForm');
    const preview = document.getElementById('preview');
    const emailBodyField = document.getElementById('emailBody');
    const subjectField = document.getElementById('subject');
    const sendBtn = document.getElementById('sendBtn');
    const loading = document.getElementById('loading');

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
        
        emailBodyField.textContent = data.email_body;
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

      sendBtn.disabled = true;
      sendBtn.textContent = 'Sending...';

      try {
        await fetch(`${API}/send-email?email_id=${emailId}&to_email=${encodeURIComponent(recipientEmail)}&subject=${encodeURIComponent(subject)}`, {
          method: 'POST'
        });

        alert('✅ Email sent successfully!');
        sendBtn.textContent = '✓ Sent';
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