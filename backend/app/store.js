import { randomUUID } from "crypto";

const EMAIL_STORE = new Map();

export function saveEmail(content) {
  const emailId = randomUUID();
  EMAIL_STORE.set(emailId, content);
  return emailId;
}

export function getEmailBody(emailId) {
  return EMAIL_STORE.get(emailId) || null;
}
