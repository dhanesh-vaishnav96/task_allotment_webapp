from app.utils.email_service import send_account_email
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.schemas import UserCreate, UserResponse,LoginRequest

router = APIRouter()
@router.post("/create-user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role="trainee"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        print("Sending email...")

        send_account_email(
            receiver_email="mish.soni.verma@gmail.com",
            trainee_name=user.name,
            trainee_email=user.email,
            password=user.password
        )

        print("Email sent successfully!")

    except Exception as e:
        print(f"Email failed: {e}")

    return new_user
@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        if existing_user.password != user.password:
            raise HTTPException(status_code=401, detail="Incorrect password")

        return {
            "success": True,
            "message": "Login Successful",
            "user_id": existing_user.id,
            "name": existing_user.name,
            "role": existing_user.role
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Server error during login: {e}")
        raise HTTPException(status_code=500, detail="Database connection error or internal server error")