#!/bin/bash
cd /home/sooraj/email-sender-genai-app/backend
source venv/bin/activate
export PYTHONPATH="/home/sooraj/email-sender-genai-app/backend:${PYTHONPATH}"
python3 gui_app.py
