import { z } from "zod";

export const EmailRequestSchema = z.object({
  recipient_email: z.string().email(),
  recipient_name: z.string(),
  recipient_position: z.string(),
  company_name: z.string(),
  company_location: z.string(),
  resume_text: z.string(),
  candidate_name: z.string(),
});

export const SendEmailRequestSchema = z.object({
  email_id: z.string(),
  to_email: z.string().email(),
  subject: z.string(),
  edited_body: z.string(),
  attachment_filename: z.string().optional(),
  attachment_content: z.string().optional(), // base64
});
