from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/auth",
    tags=["Usuarios"]
)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado.")

    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password_hash=user_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == login_data.email,
        models.User.password_hash == login_data.password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
    
    return user

@router.get("/users/{user_id}", response_model=schemas.UserProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    videos = db.query(models.Video).filter(models.Video.user_id == user_id).all()
    
    video_list = []
    for v in videos:
        video_list.append(schemas.VideoResponse(
            id=v.id,
            title=v.title,
            description=v.description,
            video_url=v.video_url,
            thumbnail_url=v.thumbnail_url,
            views=v.views,
            user_id=v.user_id,
            user_name=user.name
        ))

    return schemas.UserProfileResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        video_count=len(video_list),
        videos=video_list
    )