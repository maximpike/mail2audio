from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.schemas.email import EmailResponse
from app.services.email_parser import EmailParser
from app.services.email_service import EmailService

router = APIRouter(prefix="/emails")


# Need to insert JSON -> pydantic conversion schema object EmailCreate, EmailBase?
@router.post("/upload", response_model=EmailResponse)
async def upload_eml_file(file: UploadFile = File(...), email_service: EmailService = Depends()):
    """Upload a .eml file to ingest an email"""
    if not file.filename.endswith(".eml"):
        raise HTTPException(status_code=400, detail="Only .eml files are supported")

    # Read the file
    content = await file.read()

    # Parse it
    parsed_data = EmailParser.parse_eml_file(content)

    # Process it
    email = email_service.process_file(file)
    return email


@router.get("/", response_model=list[EmailResponse])
async def read_emails(email_service: EmailService = Depends()):
    """List all ingested emails"""
    return email_service.get_all_emails()


@router.get("/{email_id}", response_model=EmailResponse)
async def read_email(email_id: int, email_service: EmailService = Depends()):
    """Get a specific email by ID"""
    email = email_service.get_by_id(email_id)
    if not email:
        raise HTTPException(status_code=404, detail=f"Email with {email_id} not found")
    return email
