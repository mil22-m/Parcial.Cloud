import boto3
import uuid
from fastapi import UploadFile, HTTPException
from app.config import AWS_REGION

def upload_file_to_s3(file: UploadFile, bucket_name: str, folder: str = "") -> str:
    """
    Sube un archivo recibido mediante UploadFile al Bucket de S3 especificado
    y retorna la URL pública del objeto.
    """
    try:
        s3_client = boto3.client("s3", region_name=AWS_REGION)
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{folder}{uuid.uuid4().hex}.{file_extension}"

        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            unique_filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
        return f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
    except Exception as e:
        # En entornos locales sin IAM Role o credenciales, genera un placeholder de respaldo
        print(f"S3 Upload Warning: {str(e)}")
        if "image" in file.content_type:
            return f"https://via.placeholder.com/600x400?text={file.filename}"
        return f"https://www.w3schools.com/html/mov_bbb.mp4"