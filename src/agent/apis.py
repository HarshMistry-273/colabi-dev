import logging.config
from fastapi import HTTPException, Request
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database import get_db_session
from src.agent.controllers import AgentController
from sqlalchemy.orm import Session
from src.utils.logger import logger_set
import logging
from src.agent.serializers import get_agent_serializer

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()


# @router.get("")
# async def get_agents(
#     request: Request, id: str = None, db: Session = Depends(get_db_session)
# ):
#     pass


@router.put("/custom/{id}")
def update_agent(
    request: Request,
    id: int,
    db: Session = Depends(get_db_session),
):
    payload = {"id": id}
    try:
        agent = AgentController.update_agent_ctrl(db=db, payload=payload)
        agent_dict = get_agent_serializer(agent)
        logger_set.info(f"Agent updation successful, agent Id : {id}")

        return JSONResponse(
            status_code=200,
            content={
                "message": "Custom agent updated",
                "data": {"agents": agent_dict},
                "status": True,
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Could not update agent : {str(e)}")
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
        logger_set.error(f"Could not update agent : {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )
