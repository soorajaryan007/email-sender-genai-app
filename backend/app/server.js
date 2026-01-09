import express from "express";
import cors from "cors";

import { EmailRequestSchema, SendEmailRequestSchema } from "./validators.js";
import { generateColdEmail } from "./llm.js";
import { saveEmail } from "./store.js";
import { sendEmail } from "./emailService.js";

const app = express();
app.use(express.json());

app.use(
  cors({
    origin: "*",
    credentials: true,
  })
);

/**
 * POST /generate-email
 */
app.post("/generate-email", async (req, res) => {
  try {
    const data = EmailRequestSchema.parse(req.body);

    const prompt = `
Candidate Resume: ${data.resume_text}
Candidate Name: ${data.candidate_name}

Recipient Details:
Name: ${data.recipient_name}
Position: ${data.recipient_position}
Company: ${data.company_name}
Location: ${data.company_location}
`;

    const emailBody = await Promise.race([
      generateColdEmail(prompt),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Timeout")), 8000)
      ),
    ]);

    const emailId = saveEmail(emailBody);

    res.json({
      email_id: emailId,
      recipient_email: data.recipient_email,
      email_body: emailBody,
    });
  } catch (err) {
    if (err.message === "Timeout") {
      return res.status(504).json({ detail: "Email generation timed out" });
    }
    res.status(400).json({ error: err.message });
  }
});

/**
 * POST /send-email
 */
app.post("/send-email", async (req, res) => {
  try {
    const payload = SendEmailRequestSchema.parse(req.body);

    await sendEmail({
      toEmail: payload.to_email,
      subject: payload.subject,
      body: payload.edited_body,
      attachmentFilename: payload.attachment_filename,
      attachmentContent: payload.attachment_content,
    });

    res.json({
      status: "Email sent successfully",
      email_id: payload.email_id,
    });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
  console.log(`🚀 Express server running on port ${PORT}`);
});
