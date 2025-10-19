# app/email_utils.py
import os
import httpx

async def send_confirmation_email(email: str, name: str = None):
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    if not RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY not set")

    sender = "onboarding@resend.dev"
    display_name = name or "there"

    html_content = f"""
    <h1>You're on the waitlist! ✅</h1>
    <p>Hi {display_name},</p>
    <p>Your email <strong>{email}</strong> has been successfully added to our waitlist.</p>
    <p>We’ll notify you when it’s your turn. Thanks for joining!</p>
    """

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
                json={
                    "from": sender,
                    "to": email,
                    "subject": "Waitlist Confirmation ✅",
                    "html": html_content,
                },
            )
            response.raise_for_status()
            print(f"Confirmation email sent to {email}")
        except httpx.RequestError as e:
            print(f"Error sending email: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error sending email: {e.response.text}")
