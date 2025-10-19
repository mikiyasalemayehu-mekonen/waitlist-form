# app/routes/admin.py
from fastapi import APIRouter, HTTPException, Header

router = APIRouter(prefix="/api/admin", tags=["admin"])

# In a real app, move this to an environment variable!
ADMIN_PASSWORD = "yourpassword"

@router.get("/")
def read_admin(x_admin_key: str = Header(None)):
    """
    Simple password-based admin authentication using request headers.
    Frontend must send: { headers: { "x-admin-key": "yourpassword" } }
    """
    if x_admin_key != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Admin endpoint is working"}
