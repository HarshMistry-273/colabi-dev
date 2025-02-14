from datetime import datetime
import logging
from sqlalchemy.orm import Session
from database import get_db_session
from src.task.models import User
from src.user.serializers import (
    UserAttributeCreateSchema,
    get_user_attributes_serializer,
)
from src.utils.logger import logger_set
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from src.user.models import UserAttribute

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("")
async def create_user_attribute(
    request: Request,
    user_attribute: UserAttributeCreateSchema,
    db: Session = Depends(get_db_session),
):
    try:
        # Check if the user exists
        user = db.query(User).filter(User.id == user_attribute.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if UserAttribute already exists for the given user_id
        existing_user_attribute = (
            db.query(UserAttribute)
            .filter(UserAttribute.user_id == user_attribute.user_id)
            .first()
        )
        if existing_user_attribute:
            raise HTTPException(status_code=400, detail="User attribute already exists")

        # Create a new UserAttribute instance
        new_user_attribute = UserAttribute(
            user_id=user_attribute.user_id,
            attributes=user_attribute.attributes,
            created_at=user_attribute.created_at or datetime.now(),
            updated_at=user_attribute.updated_at or datetime.now(),
        )

        # Add the new UserAttribute to the session and commit
        db.add(new_user_attribute)
        db.commit()

        # Optionally, refresh the object to reflect its data after the commit
        db.refresh(new_user_attribute)
        data = get_user_attributes_serializer(new_user_attribute)
        # Return a structured JSON response with success status
        return JSONResponse(
            status_code=201,  # 201 Created
            content={
                "msg": "User attribute created successfully",
                "data": {"user_attributes": data},
                "error_msg": "",
                "error": "",
            },
        )

    except HTTPException as e:
        # Log the specific HTTPException error with context
        logger.error(f"Error occurred while creating user attribute: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": str(e.detail),
                "data": {},
                "status": False,
                "error": str(e.detail),
            },
        )

    except Exception as e:
        # Log unexpected errors with additional context
        logger.error(f"Unexpected error while creating user attribute: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


@router.get("", response_model=UserAttributeCreateSchema)
async def get_user_attribute(user_id: int, db: Session = Depends(get_db_session)):
    try:
        # Check if the user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Query the UserAttribute table for the user_id
        user_attribute = (
            db.query(UserAttribute).filter(UserAttribute.user_id == user_id).first()
        )

        if not user_attribute:
            raise HTTPException(status_code=404, detail="User attribute not found")

        # Return the user attribute details in the response
        return JSONResponse(
            status_code=200,
            content={
                "msg": "User attribute fetched successfully",
                "data": {"user_attributes": get_user_attributes_serializer(user_attribute)},
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": str(e.detail),
                "data": {},
                "status": False,
                "error": str(e.detail),
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )
