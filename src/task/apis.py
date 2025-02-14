import logging
import os
from crewai import Agent, Crew, Task
from sqlalchemy.orm import Session
from database import get_db_session
from src.config import Config
from src.utils.logger import logger_set
from fastapi.responses import FileResponse, JSONResponse
from src.task.task import reassign_task_ctrl, task_creation_celery
from fastapi import APIRouter, HTTPException, Request, Depends
from src.task.serializers import (
    CreateTaskSchema,
    completed_task_file_serializer,
    completed_task_serializer,
    reassign_completed_task_serializer
)
from src.task.controllers import (
    TaskCompletedController,
    TaskCompletedFileController,
    TaskCompletedTaskDetails,
    TaskController,
)
from textwrap import dedent
from sqlalchemy import func
from datetime import date
from langchain_openai import ChatOpenAI

router = APIRouter()

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@router.get("")
async def get_task(request: Request, id: int, db: Session = Depends(get_db_session)):
    """
    Retrieve a task by its ID and return its details as a JSON response.

    This function performs the following steps:
    1. Calls the get_tasks_ctrl function with the provided ID to retrieve the task.
    2. Constructs a JSON response containing the task's details.

    Args:
        id (str): The unique identifier of the task to retrieve.

    Returns:
        JSONResponse: A response containing the task details, including:
            - id: The task's unique identifier.
            - description: The task's description.
            - agent_id: The ID of the agent associated with the task.
            - output: The task's response or output.
            - comment: Any comments associated with the task.
            - status: The current status of the task.
            - created_at: The timestamp when the task was created (as a string).
    """
    try:
        id = request.query_params.get("id")
        logger.info("Task get endpoint")
        if id:
            tasks = TaskCompletedTaskDetails.get_completed_task_by_task_id(db, id)
        else:
            tasks = TaskCompletedTaskDetails.get_all_completed_task(db)

        task_ser = completed_task_serializer(tasks=tasks)

        for i, task in enumerate(task_ser):
            file = TaskCompletedFileController.get_completed_file_details(
                db=db, completed_task_id=task["id"]
            )
            task_ser[i]["urls"] = completed_task_file_serializer(file) if file else []

        logger_set.info("Task listed successfully.")
        return JSONResponse(
            status_code=200,
            content={
                "message": "Task fetched",
                "data": {"completed_tasks": task_ser},
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Error while fetching completed task : {str(e)}")
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
        logger_set.error(f"Error fetching tasks : {e}")
        return JSONResponse(
            status_code=500,
            content={"data": {}, "error_msg": "Invalid request", "error": str(e)},
        )


@router.post("")
def create_task(
    tasks: CreateTaskSchema, request: Request, db: Session = Depends(get_db_session)
):
    """
    Create a new task, process it using a custom agent, and return the results.

    This function performs the following steps:
    1. Creates a new task based on the provided CreateTaskSchema.
    2. Retrieves the associated agent and its tools.
    3. Initializes a CustomAgent with the agent's details and task information.
    4. Executes the task using the CustomAgent.
    5. Processes the output, including CSV file creation if required.
    6. Updates the task with the results.
    7. Returns a JSON response with the task details and outputs.

    Args:
        tasks (CreateTaskSchema): The schema containing task creation details.
        request (Request): The incoming request object.

    Returns:
        JSONResponse: A response containing the task details, outputs, and any attachments.

    Raises:
        Potential exceptions from called functions are not explicitly handled in this function.
    """
    logger.info("Task create endpoint")

    try:
        get_task = TaskController.get_tasks_by_id_ctrl(db, tasks.task_id)

        completed_task = TaskCompletedController.create_completed_task_details(
            db=db,
            task_id=get_task.id,
            from_user=tasks.from_user,
            to_user=tasks.to_user,
            from_user_role_id=tasks.from_user_role_id,
            output=None,
            comment=None,
            file_path=None,
        )
        res = task_creation_celery.delay(
            agent_id=get_task.assign_task_agent_id,
            task_id=get_task.id,
            base_url=str(request.base_url),
            include_previous_output=tasks.include_previous_output,
            previous_outputs=tasks.previous_output,
            is_csv=tasks.is_csv,
            completed_task_id=completed_task.id,
        )
        logger_set.info(
            f"Task created successfully, Task id : {get_task.id}, Agent id : {get_task.assign_task_agent_id}"
        )
        return JSONResponse(
            status_code=200,
            content={
                "message": "Task started",
                "data": {
                    "task_id": get_task.id,
                    "completed_task_id": completed_task.id,
                },
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
        logger_set.info(f"Error creating task : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


@router.post("/reassign/{completed_task_id}")
def reassign_task(completed_task_id: int, request: Request):
    logger.info("Reassign Task  endpoint")
    try:
        db = next(get_db_session())
    except:
        db = next(get_db_session())
    try:
        completed_task = TaskCompletedTaskDetails.get_completed_task_by_id(
            db=db, id=completed_task_id
        )
        if not (completed_task.status in [0, 2] and completed_task.mark_as == 2):
            raise HTTPException(status_code=401, detail="Not valid for reassignment!")

        TaskController.get_tasks_by_id_ctrl(db, completed_task.task_id)

        res = reassign_task_ctrl.delay(completed_task_id=completed_task_id)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Reassign task successful",
                "data": {
                    "task_id": completed_task.task_id,
                    "completed_task_id": completed_task.id,
                },
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"CError: {str(e)}")
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
        logger_set.info(f"Error creating task : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        ) 


@router.get("/reassign/{completed_task_id}")
def get_reassign_task(completed_task_id: int, request: Request):
    logger.info("GET Task create endpoint")
    try:
        db = next(get_db_session())
    except:
        db = next(get_db_session())
    try:
        completed_task = TaskCompletedTaskDetails.get_completed_task_by_id(
            db=db, id=completed_task_id
        )
        ct_ser = reassign_completed_task_serializer(completed_task)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Reassign task successful",
                "data": {"completed_tasks": ct_ser},
                "error_msg": "",
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
        logger_set.info(f"Error creating task : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


@router.post("/work/summary/{id}")
def summary_work_delay_task(
    request: Request, id: int, db: Session = Depends(get_db_session)
):
    try:
        summary = TaskController.summary_of_delayed_rework_task_ctrl(db=db, user_id=id)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Summary created",
                "data": {"summary": summary},
                "status": True,
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Summary for work delay and rework failed : {str(e)}")
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
        logger_set.info(f"Error creating summary : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


@router.get("/download/{file_path:path}")
def download_file(file_path: str):
    """
    Handle file download requests for CSV and Markdown files.

    This function performs the following steps:
    1. Constructs the actual file path based on the provided file_path.
    2. Checks if the file exists.
    3. Determines the media type based on the file extension.
    4. Returns a FileResponse for the requested file.

    Args:
        file_path (str): The path of the file to be downloaded, relative to the 'static' directory.

    Returns:
        FileResponse: A response containing the file content, with appropriate headers for download.
    """
    try:
        actual_path = os.path.abspath("static/" + file_path)

        # Check if the file exists
        if not os.path.isfile(actual_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Determine the media type from the file extension
        file_extension = os.path.splitext(file_path)[-1].lower()
        if file_extension == ".csv":
            media_type = "text/csv"
        elif file_extension == ".md":
            media_type = "text/markdown"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        return FileResponse(
            path=actual_path,
            filename=os.path.basename(file_path),
            media_type=media_type,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"data": {}, "error_msg": "Invalid request", "error": str(e)},
        )

# chat module
# response: dict -> agent_ids: list[int], feelancer_ids: list[int], ....
# for agent in agent_ids:db.query()
#  --> {"id", "role", ....}
#  --> openai
#  --> task -> agent selction
# freelancer, team member ///

@router.post('/create-workflow')
def create_workflow_from_opeani(details: dict):
    ...
    