from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.email_schema import EmailSchema, EmailCreate
from app.repositories.email_repository import EmailRepository
from app.services.email_parser import EmailParser

router = APIRouter(prefix="/emails")

# In-memory repo for now (will become dependency injection later)
# email_repository = EmailRepository()


@router.post("/upload", response_model=EmailSchema)
async def upload_eml_file(file: UploadFile = File(...)):
    """ Upload a .eml file to ingest an email """
    if not file.filename.endswith('.eml'):
        raise HTTPException(status_code=400, detail="Only .eml files are supported")

    # Read the file
    content = await file.read()

    # Parse it
    parsed_data = EmailParser.parse_eml_file(content)

    # Store it
    email_create = EmailCreate(**parsed_data)
    email = email_repository.create(email_create)

    return email


@router.get("/", response_model=list[EmailSchema])
async def list_emails():
    """ List all ingested emails """
    return email_repository.get_all()


@router.get("/{email_id}", response_model=EmailSchema)
async def get_email(email_id: int):
    """ Get a specific email by ID """
    email = email_repository.get_by_id(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email
