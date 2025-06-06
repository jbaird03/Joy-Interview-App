from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.email_store import load_emails, append_to_sent
from openai import OpenAI
import logging
from typing import Optional

app = FastAPI()
client = OpenAI()
logger = logging.getLogger(__name__)

MODEL = 'gpt-4o-mini'

SYSTEM_PROMPT = (
    "You are doctor Josh Levin in an outpatient clinic. I am going to provide you with emails "
    "from patients and I need you to write an email response for me.\n"
    "You should respond with an email as in this example:"
    "Subject: Re: Question About Billing\n"
    "Dear [Patient's Name],\n"
    "Thank you for reaching out regarding your bill. I understand your concern about the insurance processing. "
    "I would be happy to assist you with this matter.\n"
    "To better assist you, could you please provide me with the date of your visit and any specific details related "
    "to your insurance plan? I can then look into your billing and see if there were any issues with the claim submission.\n"
    "Alternatively, you may also want to contact your insurance provider to inquire about the status of the claim. "
    "They may provide additional insights into why it hasn't been processed yet.\n"
    "I appreciate your patience, and I look forward to resolving this for you.\n"
    "Best regards,\n Dr. Josh Levin\n Joy Clinic\n 1-800-645-7825"
)

class Email(BaseModel):
    id: str
    from_: str = Field(..., alias="from")
    patient_name: str
    subject: str
    body: str
    reply: Optional[str] = None

class SuggestRequest(BaseModel):
    body: str
    patient_name: str

@app.get("/emails")
def get_emails():
    return load_emails()

@app.post("/suggest")
def suggest_reply(request: SuggestRequest):
    user_prompt = f"{request.body}\nFrom: {request.patient_name}"
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        return {"suggested": response.choices[0].message.content}
    except Exception as e:
        logger.exception("AI suggestion failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send")
def send_email(email: Email):
    if not email.reply:
        raise HTTPException(status_code=400, detail="Reply is required to send an email.")
    append_to_sent(email.model_dump())
    return {"status": "success", "emailId": email.id}
