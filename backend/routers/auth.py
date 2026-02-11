from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from auth.jwt import create_access_token, hash_password, verify_password, get_current_user
from convex_client import ConvexClient, get_convex_client


router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    isAdmin: bool = False


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", response_model=AuthResponse)
async def register(
    body: RegisterRequest, convex: ConvexClient = Depends(get_convex_client)
):
    try:
        existing = await convex.query("users:getUserByEmail", {"email": body.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )

        # Hash the password
        password_hash = hash_password(body.password)
        
        user = await convex.mutation(
            "users:createUser",
            {
                "email": body.email,
                "passwordHash": password_hash,
                "isAdmin": body.isAdmin,
            },
        )

        token = create_access_token({"sub": user.get("_id") or str(user)})
        return AuthResponse(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest, convex: ConvexClient = Depends(get_convex_client)
):
    try:
        user = await convex.query("users:getUserByEmail", {"email": body.email})
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not verify_password(body.password, user["passwordHash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token({"sub": user.get("_id") or str(user)})
        return AuthResponse(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )


@router.get("/me")
async def me(
    current_user_id: str = Depends(get_current_user),
    convex: ConvexClient = Depends(get_convex_client),
):
    # Fetch full user object from Convex using the user ID from token
    user = await convex.query("users:getUserById", {"userId": current_user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/demo", response_model=AuthResponse)
async def demo_login(convex: ConvexClient = Depends(get_convex_client)):
    """
    Demo/test endpoint - creates or logs in with a test user account.
    Useful for testing without auth complications.
    """
    try:
        demo_email = "demo@forgerydetection.ai"
        demo_password = "demo_password_123"
        
        # Check if demo user exists
        user = await convex.query("users:getUserByEmail", {"email": demo_email})
        
        if not user:
            # Create demo user
            password_hash = hash_password(demo_password)
            user = await convex.mutation(
                "users:createUser",
                {
                    "email": demo_email,
                    "passwordHash": password_hash,
                    "isAdmin": True,  # Give demo user admin access
                },
            )
        
        token = create_access_token({"sub": user.get("_id") or str(user)})
        return AuthResponse(access_token=token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Demo login error: {str(e)}"
        )


