import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./video_platform.db")
S3_BUCKET_VIDEOS = os.getenv("S3_BUCKET_VIDEOS", "mi-plataforma-videos")
S3_BUCKET_THUMBNAILS = os.getenv("S3_BUCKET_THUMBNAILS", "mi-plataforma-thumbnails")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")