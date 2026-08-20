from auth.gmail_oauth_client import GmailOAuthClient
from config import GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES, GMAIL_TOKEN_FILE, REDIRECT_URI
from fastapi import APIRouter, Request

router = APIRouter()

oauth_client = GmailOAuthClient(
    credentials_file=GMAIL_CREDENTIALS_FILE,
    token_file=GMAIL_TOKEN_FILE,
    scopes=GMAIL_SCOPES,
    redirect_uri=REDIRECT_URI,
)


@router.get("/auth/login")
async def login():
    """Initiate OAuth flow - redirect user to Google"""
    # TODO: Generate auth URL and state
    # TODO: Save state in session
    # TODO: Redirect to Google


@router.get("/auth/callback")
async def callback(request: Request):
    """Handle OAuth callback from Google"""
    # TODO: Get code and state from query params
    # TODO: Verify state from session
    # TODO: Exchange code for token
    # TODO: Redirect to dashboard


@router.get("/auth/status")
async def status():
    pass
