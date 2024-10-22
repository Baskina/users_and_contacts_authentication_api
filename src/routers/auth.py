from fastapi import APIRouter, Depends, status, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from users_and_contacts_authentication_api.src.database.db import get_db

from users_and_contacts_authentication_api.src.repository import users as repository_users
from users_and_contacts_authentication_api.src.schemas.users import UserValidationSchemaResponse, UserValidationSchema, TokenSchema
from users_and_contacts_authentication_api.src.services.auth import auth_service

router = APIRouter(prefix='/auth', tags=['auth'])

get_refresh_token = HTTPBearer()


@router.post("/signup", response_model=UserValidationSchemaResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserValidationSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.hash = auth_service.get_password_hash(body.hash)
    new_user = await repository_users.create_user(body, db)
    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.verify_password(body.password, user.hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(get_refresh_token), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
