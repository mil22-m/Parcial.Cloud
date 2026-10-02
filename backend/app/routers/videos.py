from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.s3_utils import upload_file_to_s3
from app.config import S3_BUCKET_VIDEOS, S3_BUCKET_THUMBNAILS

router = APIRouter(tags=["Videos"])

@router.get("/videos", response_model=List[schemas.VideoResponse])
def get_all_videos(db: Session = Depends(get_db)):
    videos = db.query(models.Video).all()
    result = []
    for v in videos:
        result.append(schemas.VideoResponse(
            id=v.id,
            title=v.title,
            description=v.description,
            video_url=v.video_url,
            thumbnail_url=v.thumbnail_url,
            views=v.views,
            user_id=v.user_id,
            user_name=v.owner.name if v.owner else "Anónimo"
        ))
    return result

@router.post("/videos", response_model=schemas.VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
    title: str = Form(...),
    description: Optional[str] = Form(""),
    user_id: int = Form(...),
    video_file: UploadFile = File(...),
    thumbnail_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    video_url = upload_file_to_s3(video_file, S3_BUCKET_VIDEOS, folder="videos/")
    thumbnail_url = upload_file_to_s3(thumbnail_file, S3_BUCKET_THUMBNAILS, folder="thumbnails/")

    new_video = models.Video(
        title=title,
        description=description,
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        user_id=user_id
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    return schemas.VideoResponse(
        id=new_video.id,
        title=new_video.title,
        description=new_video.description,
        video_url=new_video.video_url,
        thumbnail_url=new_video.thumbnail_url,
        views=new_video.views,
        user_id=new_video.user_id,
        user_name=new_video.owner.name if new_video.owner else "Anónimo"
    )

@router.get("/videos/{video_id}", response_model=schemas.VideoDetailResponse)
def get_video_by_id(video_id: int, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado.")

    # Incrementar las reproducciones / vistas
    video.views += 1
    db.commit()

    # Cargar videos recomendados (excluyendo el actual)
    recommended_raw = db.query(models.Video).filter(models.Video.id != video_id).limit(5).all()
    recommended = [
        schemas.VideoResponse(
            id=r.id,
            title=r.title,
            description=r.description,
            video_url=r.video_url,
            thumbnail_url=r.thumbnail_url,
            views=r.views,
            user_id=r.user_id,
            user_name=r.owner.name if r.owner else "Anónimo"
        ) for r in recommended_raw
    ]

    return schemas.VideoDetailResponse(
        id=video.id,
        title=video.title,
        description=video.description,
        video_url=video.video_url,
        thumbnail_url=video.thumbnail_url,
        views=video.views,
        user_id=video.user_id,
        user_name=video.owner.name if video.owner else "Anónimo",
        recommended=recommended
    )

@router.put("/videos/{video_id}", response_model=schemas.VideoResponse)
def update_video(
    video_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(""),
    db: Session = Depends(get_db)
):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado.")

    video.title = title
    video.description = description
    db.commit()
    db.refresh(video)

    return schemas.VideoResponse(
        id=video.id,
        title=video.title,
        description=video.description,
        video_url=video.video_url,
        thumbnail_url=video.thumbnail_url,
        views=video.views,
        user_id=video.user_id,
        user_name=video.owner.name if video.owner else "Anónimo"
    )

@router.delete("/videos/{video_id}")
def delete_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado.")

    db.delete(video)
    db.commit()
    return {"message": "Video eliminado correctamente."}