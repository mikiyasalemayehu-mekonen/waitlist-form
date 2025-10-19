import os
import httpx

async def send_confirmation_email(email: str):
    RESEND_API_KEY = os.getenv("RESEND_API_KEY")
    if not RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY not set")

    sender = "onboarding@resend.dev"

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
                json={
                    "from": sender,
                    "to": email,
                    "subject": "Welcome to the Waitlist!",
                    "html": "<strong>Thank you for signing up!</strong>",
                },
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Error sending email: {e}")
