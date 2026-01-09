import nodemailer from "nodemailer";

export async function sendEmail({
  toEmail,
  subject,
  body,
  attachmentFilename,
  attachmentContent,
}) {
  const { SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD } = process.env;

  if (!SMTP_HOST || !SMTP_PORT || !SMTP_EMAIL || !SMTP_PASSWORD) {
    throw new Error("SMTP configuration missing");
  }

  const transporter = nodemailer.createTransport({
    host: SMTP_HOST,
    port: Number(SMTP_PORT),
    secure: true,
    auth: {
      user: SMTP_EMAIL,
      pass: SMTP_PASSWORD,
    },
  });

  const mailOptions = {
    from: SMTP_EMAIL,
    to: toEmail,
    subject,
    text: body,
    attachments:
      attachmentFilename && attachmentContent
        ? [
            {
              filename: attachmentFilename,
              content: Buffer.from(attachmentContent, "base64"),
            },
          ]
        : [],
  };

  await transporter.sendMail(mailOptions);
}
