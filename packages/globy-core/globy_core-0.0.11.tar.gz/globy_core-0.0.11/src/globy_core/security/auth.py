from datetime import datetime, timedelta
from typing import Optional
import jwt
from pydantic import BaseModel
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

class User(BaseModel):
    email: str
    password: str
    verified: bool

class EmailRequest(BaseModel):
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class AuthManager:
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self):
        self.users_db = {}
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except jwt.PyJWTError:
            raise credentials_exception
        user = self.users_db.get(token_data.email)
        if user is None:
            raise credentials_exception
        return user

    async def signup(self, user: User):
        if user.email in self.users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        self.users_db[user.email] = user.model_dump()
        self.send_mock_email(user.email, 'Confirm your email', 'Please confirm your email.')
        return user

    async def confirm(self, request: EmailRequest):
        user_email = request.email
        user = self.users_db.get(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user['verified'] = True
        self.users_db[user_email] = user
        return {"message": "Email confirmed"}

    async def login(self, form_data: OAuth2PasswordRequestForm):
        user = self.users_db.get(form_data.username)
        if not user or user['password'] != form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user['verified']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email not verified",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user['email']}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def send_mock_email(self, to_address, subject, body):
        print(f"Sending email to {to_address}: {subject} - {body}")