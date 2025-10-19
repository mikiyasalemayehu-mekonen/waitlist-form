# app/routes/waitlist.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from app.models import Waitlist
from app.email_utils import send_confirmation_email
import os
from app.schemas import WaitlistCreate, WaitlistResponse
from app.database import SessionLocal



router = APIRouter(prefix="/api/waitlist", tags=["waitlist"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/", response_model=WaitlistResponse)
def add_email(data: WaitlistCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(Waitlist).filter(Waitlist.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_entry = Waitlist(email=data.email)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    background_tasks.add_task(send_confirmation_email, data.email)
    return new_entry



# ✅ Secure route for admin access
@router.get("/secure")
def get_waitlist_secure(
    x_admin_key: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Secure admin-only endpoint to view all waitlist entries.
    Requires 'x-admin-key' header to match ADMIN_PASSWORD.
    """
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    if x_admin_key != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

    entries = db.query(Waitlist).order_by(Waitlist.created_at.desc()).all()
    return entries


def send_confirmation_email(to_email: str):
    print(f"Sending confirmation email to {to_email}")
