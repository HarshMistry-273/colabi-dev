from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
from src.user.models import UserAttribute

class UserAttributeCreateSchema(BaseModel):
    user_id: int
    attributes: Optional[List[Dict]] = None  # JSON field for attributes
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    # class Config:
    #     from_attributes = True  # Allows the conversion from ORM models to Pydantic models


def get_user_attributes_serializer(uzr_attrs: list[UserAttribute]) -> list[dict]:
    uzr_attr_list = []

    if not isinstance(uzr_attrs, list):
        uzr_attrs = [uzr_attrs]
    for uzr_attr in uzr_attrs:
        uzr_attr_dict = {
            # Primary Key
            "id": uzr_attr.id,
            "customers": uzr_attr.attributes,
            "created_at": str(uzr_attr.created_at),
            "updated_at": str(uzr_attr.updated_at),
        }
        uzr_attr_list.append(uzr_attr_dict)

    return uzr_attr_list