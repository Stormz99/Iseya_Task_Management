from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db
from app.models.user import User
from app.auth.hashing import Hash
from app.auth.jwt import create_access_token, get_current_user
from app.auth.schemas import RegisterSchema, LoginSchema


auth_router = APIRouter(tags=["Authentication"])

# REGISTER USER
@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: RegisterSchema, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).filter(User.email == request.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = Hash.bcrypt(request.password)

    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        role=request.role or "user"
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


# **Fixed LOGIN USER to Accept JSON in Swagger**
@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(request: LoginSchema, db: AsyncSession = Depends(get_db)):
    # Query user by email
    result = await db.execute(select(User).filter(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user or not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    # Generate JWT token
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}
