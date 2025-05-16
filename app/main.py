from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app.schemas import UserCreate, Token
from app.auth.oauth2 import get_oauth_client
from app.auth.jwt import create_access_token, verify_token
from app.auth.password import get_password_hash, authenticate_user
from app.auth.security import JWTBearer, generate_state_token, verify_state_token
from app.crud.users import create_or_update_user, get_user_by_email, create_user
from app.auth.cookie_utils import set_cookie
from config import settings

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Authentication Routes ---
@app.post("/auth/register", response_model=Token)
async def register_user(
    user_data: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    """Register new user with email/password"""
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user_data.password)
    user = create_user(db, user_data, hashed_password)
    access_token = create_access_token({"sub": user.email})
    set_cookie(response, "access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Email/password login"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token({"sub": user.email})
    set_cookie(response, "access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/oauth/{provider}")
async def start_oauth(provider: str):
    """Initiate OAuth2 flow"""
    oauth = await get_oauth_client(provider)
    state = generate_state_token()
    auth_url = await oauth.get_authorize_url(state=state)
    
    response = Response(status_code=status.HTTP_200_OK)
    set_cookie(response, "oauth_state", state, expires_minutes=5)
    return {"auth_url": auth_url}

@app.get("/auth/oauth/{provider}/callback")
async def oauth_callback(
    provider: str,
    request: Request,
    code: str,
    state: str,
    db: Session = Depends(get_db)
):
    """OAuth2 callback endpoint"""
    # CSRF protection
    if not verify_state_token(state) or state != request.cookies.get("oauth_state"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state token"
        )
    
    # Exchange code for token
    oauth = await get_oauth_client(provider)
    token = await oauth.get_access_token(code)
    user_data = await oauth.get_user_info(token)
    
    # Create/update user
    user = create_or_update_user(db, user_data["email"])
    
    # Set JWT cookie
    access_token = create_access_token({"sub": user.email})
    response = Response(status_code=status.HTTP_200_OK)
    set_cookie(response, "access_token", access_token)
    response.delete_cookie("oauth_state")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/logout")
async def logout_user(response: Response):
    """Clear authentication cookies"""
    response = Response(status_code=status.HTTP_200_OK)
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}

# --- Protected Routes ---
@app.get("/users/me", dependencies=[Depends(JWTBearer())])
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get current user details"""
    token = request.cookies.get("access_token")
    payload = verify_token(token)
    user = get_user_by_email(db, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# --- Health Check ---
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
