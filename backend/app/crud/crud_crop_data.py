from sqlalchemy.orm import Session
from app.models.crop_data import CropData
from app.schemas.crop_data import CropDataCreate

class CRUDCropData:
    def get_crop_by_name(self, db: Session, name: str):
        return db.query(CropData).filter(CropData.crop_name == name).first()

    def get_all_crops(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(CropData).offset(skip).limit(limit).all()

    def create_crop(self, db: Session, *, crop_in: CropDataCreate):
        db_crop = CropData(**crop_in.dict())
        db.add(db_crop)
        db.commit()
        db.refresh(db_crop)
        return db_crop

crop_data = CRUDCropData()
