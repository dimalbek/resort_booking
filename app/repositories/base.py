from typing import TypeVar, Generic, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Any

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(
        self, db: Session, obj_in: CreateSchemaType | dict[str, Any]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            data: dict[str, Any] = obj_in
        else:
            data = obj_in.dict()
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        update_data = (
            obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> None:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
