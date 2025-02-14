import logging
from sqlalchemy.orm import Session
from database import get_db_session
from src.utils.logger import logger_set
from fastapi.responses import JSONResponse
from src.tool.controllers import ToolsController, insert_if_all_listed_tools_does_not_exist
from fastapi import APIRouter, Depends, HTTPException, Request
from src.tool.serializers import UpdateToolSchema, get_tools_serializer

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()

insert_if_all_listed_tools_does_not_exist()


@router.put("/{id}")
def update_tools(
    request: Request,
    payload: UpdateToolSchema,
    id: str,
    db: Session = Depends(get_db_session),
):
    try:
        tools = ToolsController.update_tools(db=db, id=id, payload=payload.model_dump())

        tools_json = get_tools_serializer(tools=tools)
        logger_set.info(f"Tool Updated: ID: {id}")

        return JSONResponse(
            status_code=200,
            content={
                "msg": "Tool updated",
                "data": {"tools": tools_json},
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Error occured updating tool : {str(e)}, ToolID: {id}")
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
        logger_set.error(f"Error getting tool : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


@router.get("")
async def get_tools(request: Request):
    try:
        try:
            db = next(get_db_session())
        except :
            db = next(get_db_session())

        id = request.query_params.get("id")

        if id:
            tools = ToolsController.get_tool_by_uuid(db=db, id=id)
        else:
            tools = ToolsController.get_all_tools(db)

        tools_json = get_tools_serializer(tools=tools)
        logger_set.info(f"Tools listed")
        return JSONResponse(
            status_code=200,
            content={
                "msg": "Tool fetched",
                "data": {"tools": tools_json},
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Error occured while fetching tool : {str(e)}")
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
        logger_set.error(f"Error getting tool : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )
