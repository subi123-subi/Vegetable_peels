import secrets
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.scan import ScanRecord, ScanPrediction, UserConfirmation
from app.models.vegetable import Vegetable
from app.schemas.user import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse,
    UserProfileUpdate,
    PasswordChange,
    PasswordResetRequest,
    PasswordResetConfirm,
    UserHistoryItem,
)

router = APIRouter()

# In-memory token store for demonstration password reset workflow
_RESET_TOKENS: dict[str, str] = {}


def get_or_create_default_role(db: Session, role_name: str = "user") -> UserRole:
    role = db.query(UserRole).filter(UserRole.name == role_name).first()
    if not role:
        role = UserRole(name=role_name, description=f"Standard {role_name} permissions")
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    role = get_or_create_default_role(db, "user")
    new_user = User(
        email=payload.email.strip().lower(),
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name.strip(),
        role_id=role.id,
        preferred_language=payload.preferred_language,
        is_active=True,
        is_superuser=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        role_name=role.name,
        is_active=new_user.is_active,
        is_superuser=new_user.is_superuser,
        preferred_language=new_user.preferred_language,
        created_at=new_user.created_at,
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate and receive JWT Bearer token",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account.",
        )

    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role_name=current_user.role.name if current_user.role else "user",
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        preferred_language=current_user.preferred_language,
        created_at=current_user.created_at,
    )


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
def update_me(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name.strip()
    if payload.preferred_language is not None:
        current_user.preferred_language = payload.preferred_language

    db.commit()
    db.refresh(current_user)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role_name=current_user.role.name if current_user.role else "user",
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        preferred_language=current_user.preferred_language,
        created_at=current_user.created_at,
    )


@router.put(
    "/me/password",
    status_code=status.HTTP_200_OK,
    summary="Change user password",
)
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(payload.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password.",
        )

    current_user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    return {"message": "Password updated successfully."}


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete account and user data (Privacy & GDPR compliance)",
)
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.delete(current_user)
    db.commit()
    return None


@router.get(
    "/history",
    response_model=List[UserHistoryItem],
    summary="Get authenticated user's scan history and reports",
)
def get_user_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scans = (
        db.query(ScanRecord)
        .options(
            joinedload(ScanRecord.predictions).joinedload(ScanPrediction.predicted_vegetable),
            joinedload(ScanRecord.confirmation).joinedload(UserConfirmation.confirmed_vegetable),
        )
        .filter(ScanRecord.user_id == current_user.id)
        .order_by(desc(ScanRecord.scanned_at))
        .limit(limit)
        .all()
    )

    results = []
    for s in scans:
        top_pred = s.predictions[0] if s.predictions else None
        conf = s.confirmation

        veg = None
        if conf and conf.confirmed_vegetable:
            veg = conf.confirmed_vegetable
        elif top_pred and top_pred.predicted_vegetable:
            veg = top_pred.predicted_vegetable

        results.append(
            UserHistoryItem(
                scan_id=s.id,
                image_path=s.image_path,
                vegetable_slug=veg.slug if veg else None,
                vegetable_name_en=veg.name_en if veg else "Unknown",
                vegetable_name_ta=veg.name_ta if veg else "தெரியாதது",
                confidence=top_pred.confidence if top_pred else 0.0,
                is_confirmed=conf is not None,
                confirmed_weight_grams=conf.confirmed_weight_grams if conf else None,
                scanned_at=s.scanned_at,
            )
        )
    return results


@router.post(
    "/password-reset/request",
    summary="Request a password reset token",
)
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user:
        # Avoid user enumeration by returning standard response
        return {"message": "If the account exists, a reset token has been issued."}

    token = secrets.token_urlsafe(32)
    _RESET_TOKENS[user.email] = token
    return {
        "message": "If the account exists, a reset token has been issued.",
        "reset_token": token,  # Provided for immediate testing & CLI
    }


@router.post(
    "/password-reset/confirm",
    summary="Confirm password reset with token",
)
def confirm_password_reset(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    stored_token = _RESET_TOKENS.get(email)
    if not stored_token or stored_token != payload.reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token.",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    del _RESET_TOKENS[email]

    return {"message": "Password reset successfully. You may now log in with your new password."}
