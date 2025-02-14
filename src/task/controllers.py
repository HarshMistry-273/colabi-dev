from datetime import datetime
from crewai import Agent, Crew, Task
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.config import Config
from src.task.models import (
    CompletedTaskDetailFiles,
    TaskUser,
    Tasks,
    CompletedTaskDetails,
    WorkFlow,
    User,
)
from textwrap import dedent
from sqlalchemy import func
from datetime import date
from langchain_openai import ChatOpenAI


class TaskController:

    @staticmethod
    def get_tasks_by_id_ctrl(db: Session, id: int) -> Tasks:
        task = db.query(Tasks).filter(Tasks.id == id).first()

        if task:
            return task

        raise HTTPException(detail="Task not found", status_code=404)

    @staticmethod
    def summary_of_delayed_rework_task_ctrl(db: Session, user_id: int) -> str:

        users_tasks = db.query(TaskUser).filter(TaskUser.user_id == user_id).all()

        if not users_tasks:
            raise HTTPException(detail="User has no task", status_code=404)

        task_ids = [
            task_id.task_id for task_id in users_tasks if task_id.user_id == user_id
        ]

        delay_query = (
            db.query(
                Tasks.id,
                Tasks.assign_task_team_member_id,
                Tasks.workflow_id,
                Tasks.completion_date,
                WorkFlow.title,
                func.datediff(func.current_date(), Tasks.completion_date).label(
                    "delay_duration"
                ),
                User.name,
            )
            .join(WorkFlow, Tasks.workflow_id == WorkFlow.id, isouter=True)
            .join(User, Tasks.assign_task_team_member_id == User.id, isouter=True)
            .filter(Tasks.id.in_(task_ids))
            .filter(Tasks.status != "Completed")
            .filter(Tasks.completion_date < date.today())
        ).all()
        delay_data = []
        print("Delayed task...", len(delay_query))
        for i in delay_query:
            delay_data.append(
                {
                    "task_id": i[0],
                    "assign_task_team_memeber_id": i[1],
                    "workflow_id": i[2],
                    "completion_date": i[3],
                    "title": i[4],
                    "delay_duration": i[5],
                    "name": i[6],
                }
            )
        completed_query = (
            db.query(
                Tasks.id,
                Tasks.assign_task_team_member_id,
                Tasks.workflow_id,
                Tasks.completion_date,
                WorkFlow.title,
                User.name,
            )
            .join(WorkFlow, Tasks.workflow_id == WorkFlow.id, isouter=True)
            .join(User, Tasks.assign_task_team_member_id == User.id, isouter=True)
            .filter(Tasks.id.in_(task_ids))
            .filter(Tasks.status == "Completed")
        ).all()
        completed_data = []
        print("Completed task...", len(completed_query))
        for i in completed_query:
            completed_data.append(
                {
                    "task_id": i[0],
                    "assign_task_team_memeber_id": i[1],
                    "workflow_id": i[2],
                    "completion_date": i[3],
                    "title": i[4],
                    "name": i[5],
                }
            )

        rework_query = (
            db.query(
                CompletedTaskDetails.id,
                CompletedTaskDetails.task_id,
                CompletedTaskDetails.mark_as,
                Tasks.agent_instruction,
                Tasks.agent_output,
                CompletedTaskDetails.output,
                CompletedTaskDetails.status,
                CompletedTaskDetails.reason_for_reassign,
            )
            .join(Tasks, CompletedTaskDetails.task_id == Tasks.id, isouter=True)
            .filter(CompletedTaskDetails.mark_as == 2)
        ).all()

        print("Delayed task...", len(rework_query))
        rework_data = []

        for i in rework_query:
            rework_data.append(
                {
                    "completed_task_id": i[0],
                    "task_id": i[1],
                    "mark_as": i[2],
                    "agent_instruction": i[3],
                    "expected_output": i[4],
                    "output": i[5],
                    "status": i[6],
                }
            )

        llm = ChatOpenAI(model=Config.MODEL_NAME, api_key=Config.OPENAI_API_KEY)

        data_analyst = Agent(
            role="Senior Data Analyst",
            goal="You receive data from the database developer and analyze it",
            backstory=dedent(
                """
            You have deep experience with analyzing datasets using Python.
            Your work is always based on the provided data and is clear,
            easy-to-understand and to the point. You have attention
            to detail and always produce very detailed work (as long as you need).
        """
            ),
            llm=llm,
            allow_delegation=False,
        )

        analyze_data = Task(
            description="Analyze the data from the database and write an analysis for Completed Data: {completed_data}, Total completed task: {total_completed_tasks} Delayed Data: {delay_data}, Total Delayed Task: {total_delayed_tasks}, Rework Data: {rework_data} and Total Rework Tasks: {total_rework_tasks}, ",
            # expected_output="Analyze the provided data, generating a succinct narrative highlighting key performance metrics, task outcomes, and critical insights. Provide a straightforward assessment using a list or string format, focusing on concrete observations without speculative language.",
            expected_output="Analysis of the data as a list of string. Analysis example can be: Your team completed 45 tasks today, with 3 delays and 5 reworks... Strict Note: Do not provide markdown output. Keep output short and precise as shown in example. Do NOT use phrases like 'further analysis is needed' or similar, Instead, you must directly analyze the given data with the available information and provide a clear conclusion based on that data. ",
            agent=data_analyst,
            # context=[extract_data],
        )

        crew = Crew(
            agents=[data_analyst],
            tasks=[analyze_data],
            # process=Process.sequential,
            verbose=False,
            memory=False,
            output_log_file="crew.log",
        )

        inputs = {
            "delay_data": str(delay_data),
            "total_delayed_tasks": len(delay_query),
            "rework_data": str(rework_data),
            "total_rework_tasks": len(rework_query),
            "completed_data": str(completed_data),
            "total_completed_tasks": len(completed_query),
        }

        result = crew.kickoff(inputs=inputs)

        return result.raw


class TaskCompletedController:
    @staticmethod
    def get_completed_task_details_by_task_id(
        db: Session, task_id: int
    ) -> CompletedTaskDetails:
        completed_task = (
            db.query(CompletedTaskDetails)
            .filter(CompletedTaskDetails.task_id == task_id)
            .first()
        )

        if completed_task:
            return completed_task

        raise HTTPException(detail="Completed task not found", status_code=404)

    @staticmethod
    def get_completed_task_details_by_id(db: Session, id: int) -> CompletedTaskDetails:
        completed_task = (
            db.query(CompletedTaskDetails).filter(CompletedTaskDetails.id == id).first()
        )

        if completed_task:
            return completed_task

        raise HTTPException(detail="Completed task not found", status_code=404)

    @staticmethod
    def create_completed_task_details(
        db: Session,
        task_id: int,
        from_user: int,
        to_user: int,
        from_user_role_id: int,
        output: str,
        comment: str,
        file_path: str,
    ) -> CompletedTaskDetails:
        completed_task = CompletedTaskDetails(
            task_id=task_id,
            from_user=from_user,
            to_user=to_user,
            from_user_role_id=from_user_role_id,
            output=output,
            comment=comment,
            status=0,
            created_at=datetime.now(),
        )

        try:
            db.add(completed_task)
            db.commit()
            db.refresh(completed_task)
        except Exception as e:
            db.rollback()  # Make sure to rollback the transaction
            raise HTTPException(detail="Database error: " + str(e), status_code=400)

        if file_path:
            create_file = TaskCompletedFileController.create_completed_file_details(
                db, completed_task_id=completed_task.id, file_path=file_path
            )

            if not create_file:
                # Handle case where file creation fails
                raise HTTPException(
                    detail="Failed to associate file with completed task",
                    status_code=500,
                )

        return completed_task

    @staticmethod
    def update_completed_task_details(
        db: Session,
        completed_task_id: int,
        success: bool,
        status: bool = None,
        mark_as: int = None,
        output: str = None,
        comment: str = None,
        file_path: str = None,
    ) -> CompletedTaskDetails:

        completed_task = TaskCompletedController.get_completed_task_details_by_id(
            db=db, id=completed_task_id
        )
        completed_task.output = output
        completed_task.comment = comment
        completed_task.updated_at = datetime.now()
        if success == True:
            completed_task.status = status
            completed_task.mark_as = mark_as

        try:
            db.commit()
        except Exception as e:
            raise HTTPException(detail=f"Database error: {str(e)}", status_code=400)

        if file_path:
            create_file = TaskCompletedFileController.create_completed_file_details(
                db, completed_task_id=completed_task.id, file_path=file_path
            )

            if not create_file:
                ...

        return completed_task
    
    @staticmethod
    def update_completed_task_details_with_marked_as(
        db: Session,
        completed_task_id: int,
        status: int,
        mark_as: int,
        output: str = None,
        comment: str = None,
        file_path: str = None,
    ) -> CompletedTaskDetails:

        completed_task = TaskCompletedController.get_completed_task_details_by_id(
            db=db, id=completed_task_id
        )
        completed_task.output = output
        completed_task.comment = comment
        completed_task.status = status
        completed_task.mark_as = mark_as
        completed_task.updated_at = datetime.now()

        try:
            db.commit()
        except Exception as e:
            raise HTTPException(detail=f"Database error: {str(e)}", status_code=400)

        if file_path:
            create_file = TaskCompletedFileController.create_completed_file_details(
                db, completed_task_id=completed_task.id, file_path=file_path
            )

            if not create_file:
                ...

        return completed_task


class TaskCompletedTaskDetails:
    @staticmethod
    def get_completed_task_by_id(db: Session, id: int = None):
        completed_task = (
            db.query(CompletedTaskDetails).filter(CompletedTaskDetails.id == id).first()
        )

        if completed_task:
            return completed_task
        raise HTTPException(detail="Completed task not found", status_code=404)

    @staticmethod
    def get_completed_task_by_task_id(db: Session, id: int = None):
        completed_task = (
            db.query(CompletedTaskDetails)
            .filter(CompletedTaskDetails.task_id == id)
            .order_by(CompletedTaskDetails.created_at.desc())
            .all()
        )

        if completed_task:
            return completed_task
        raise HTTPException(detail="Completed task not found", status_code=404)

    @staticmethod
    def get_all_completed_task(db: Session):
        completed_task = db.query(CompletedTaskDetails).all()

        return completed_task


class TaskCompletedFileController:
    @staticmethod
    def create_completed_file_details(
        db: Session, completed_task_id: int, file_path: str
    ) -> CompletedTaskDetailFiles:
        com_task_file = CompletedTaskDetailFiles(
            completed_task_detail_id=completed_task_id,
            file_name=file_path,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        try:
            db.add(com_task_file)
            db.commit()
            db.refresh(com_task_file)
        except Exception as e:
            raise HTTPException(detail=f"Database error: {str(e)}", status_code=400)
        return com_task_file

    @staticmethod
    def get_completed_file_details(
        db: Session, completed_task_id: int
    ) -> CompletedTaskDetailFiles:
        file_details = (
            db.query(CompletedTaskDetailFiles)
            .filter(
                CompletedTaskDetailFiles.completed_task_detail_id == completed_task_id
            )
            .first()
        )

        return file_details


class TaskUtils:
    @staticmethod
    def get_previous_outputs(db: Session, previous_outputs):
        previous_output = []
        res_opt_tsk_id = None
        for prev_task_id in previous_outputs:
            response_output = TaskCompletedController.get_completed_task_details_by_id(
                db=db, id=prev_task_id
            )

            if res_opt_tsk_id == None:
                res_opt_tsk_id = response_output.task_id
                output = TaskController.get_tasks_by_id_ctrl(db=db, id=res_opt_tsk_id)
            elif res_opt_tsk_id != response_output.task_id:
                res_opt_tsk_id = response_output.task_id
                output = TaskController.get_tasks_by_id_ctrl(db=db, id=res_opt_tsk_id)
            previous_output.append(
                f"""
                    agent_instruction : {output.agent_instruction},
                    expected_output: {output.agent_output},
                    response: {response_output.output},
                """
            )

        return previous_output
    
    @staticmethod
    def get_previous_outputs_by_completed_task(db: Session, previous_outputs):
        previous_output = []
        res_opt_tsk_id = None
        for prev_task_id in previous_outputs:
            response_output = TaskCompletedController.get_completed_task_details_by_id(
                db=db, id=prev_task_id
            )

            if res_opt_tsk_id == None:
                res_opt_tsk_id = response_output.task_id
                output = TaskController.get_tasks_by_id_ctrl(db=db, id=response_output.task_id)
            elif res_opt_tsk_id != response_output.task_id:
                res_opt_tsk_id = response_output.task_id
                output = TaskController.get_tasks_by_id_ctrl(db=db, id=res_opt_tsk_id)
            previous_output.append(
                f"""
                    agent_instruction : {output.agent_instruction},
                    expected_output: {output.agent_output},
                    response: {response_output.output},
                """ 
            )

        return previous_output
