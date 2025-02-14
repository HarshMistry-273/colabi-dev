from typing import Optional
from pydantic import BaseModel
from src.task.models import CompletedTaskDetailFiles, Tasks, CompletedTaskDetails
from src.config import Config


class CreateTaskSchema(BaseModel):
    task_id: int
    from_user: int
    to_user: int
    from_user_role_id: int
    include_previous_output: Optional[bool] = False
    previous_output: Optional[list[int]] = []
    is_csv: Optional[bool] = False

class ReassignTaskSchema(BaseModel):
    completed_task_id: int
    include_previous_output: Optional[bool] = False
    previous_output: Optional[list[int]] = []
    is_csv: Optional[bool] = False


def task_serializer(tasks: list[Tasks]) -> list[dict]:
    tasks_list = []

    if not isinstance(tasks, list):
        tasks = [tasks]

    for task in tasks:
        tasks_list.append(
            {
                "id": task.id,
                "parent_task_id": task.parent_task_id,
                "job_id": task.job_id,
                "workflow_id": task.workflow_id,
                "category_id": task.category_id,
                "uuid": task.uuid,
                "title": task.title,
                "description": task.description,
                "start_date": str(task.start_date),
                "video_file": task.video_file,
                "completion_date": str(task.completion_date),
                "reoccurring": task.reoccurring,
                "assign_task_agent_id": task.assign_task_agent_id,
                "agent_tool": task.agent_tool,
                "agent_instruction": task.agent_instruction,
                "agent_output": task.agent_output,
                "agent_parameter": task.agent_parameter,
                "assign_task_team_member_id": task.assign_task_team_member_id,
                "team_member_ai_agent_for_assistance": task.team_member_ai_agent_for_assistance,
                "team_member_instruction": task.team_member_instruction,
                "team_member_output": task.team_member_output,
                "assign_task_colabi_member_id": task.assign_task_colabi_member_id,
                "colabi_member_ai_agent_for_assistance": task.colabi_member_ai_agent_for_assistance,
                "colabi_member_instruction": task.colabi_member_instruction,
                "colabi_member_output": task.colabi_member_output,
                "assign_task_my_self_id": task.assign_task_my_self_id,
                "my_self_ai_agent_for_assistance": task.my_self_ai_agent_for_assistance,
                "my_self_instruction": task.my_self_instruction,
                "my_self_output": task.my_self_output,
                "assign_task_client_id": task.assign_task_client_id,
                "client_ai_agent_for_assistance": task.client_ai_agent_for_assistance,
                "client_instruction": task.client_instruction,
                "client_output": task.client_output,
                "created_at": str(task.created_at),
                "updated_at": str(task.updated_at),
                "created_by": str(task.created_by),
                "status": task.status,
                "start_time": str(task.start_time),
                "end_time": str(task.end_time),
                "assign_to": task.assign_to,
            }
        )

    return tasks_list


def completed_task_serializer(tasks: list[CompletedTaskDetails]) -> list[dict]:
    tasks_list = []

    if not isinstance(tasks, list):
        tasks = [tasks]

    for task in tasks:
        tasks_list.append(
            {
                # Primary and Foreign Keys
                "id": task.id,
                "task_id": task.task_id if task.task_id else "",
                "from_user": task.from_user if task.from_user else "",
                "to_user": task.to_user if task.to_user else "",
                "from_user_role_id": (
                    task.from_user_role_id if task.from_user_role_id else ""
                ),
                "output": task.output if task.output else "",
                "comment": task.comment if task.comment else "",
                "status": task.status if task.status else "",
                "mark_as": task.mark_as if task.mark_as else "",
                "reason_for_reassign": (
                    task.reason_for_reassign if task.reason_for_reassign else ""
                ),
                "created_at": str(task.created_at) if task.created_at else "",
                "updated_at": str(task.updated_at) if task.updated_at else "",
            }
        )

    return tasks_list


def reassign_completed_task_serializer(tasks: list[CompletedTaskDetails]) -> list[dict]:
    tasks_list = []

    if not isinstance(tasks, list):
        tasks = [tasks]

    for task in tasks:
        tasks_list.append(
            {
                # Primary and Foreign Keys
                "id": task.id,
                "task_id": task.task_id if task.task_id else "",
                "status": task.status if task.status else "",
                "mark_as": task.mark_as if task.mark_as else "",
            }
        )

    return tasks_list



def completed_task_file_serializer(files: list[CompletedTaskDetailFiles]) -> list[dict]:
    files_list = []

    if not isinstance(files, list):
        files = [files]

    for file in files:
        files_list.append(
            {
                # Primary and Foreign Keys
                "id": file.id,
                "completed_task_detail_id": file.completed_task_detail_id,
                "file_name": file.file_name,
                "created_at": str(file.created_at),
                "updated_at": str(file.updated_at),
            }
        )

    return files_list
