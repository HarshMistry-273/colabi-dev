import json
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.crew.tools import ToolKit
from src.tool.models import Tools
from database import db
import logging

from src.utils.utils import get_uuid

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def validate_tool_parameters(parameters: str) -> bool:
    """
    Validates that the parameters string is valid JSON.
    Returns True if valid, False otherwise.
    """
    try:
        json.loads(parameters)
        return True
    except json.JSONDecodeError:
        return False


def insert_if_all_listed_tools_does_not_exist():
    existing_tools = [tool_name.name for tool_name in ToolKit]
    tools_db = db.query(Tools).all()

    if len(existing_tools) != len(tools_db):
        logging.info("Seem we have new tools in toolkit.")

        for tool_db in tools_db:
            if tool_db.tool_name in existing_tools:
                try:
                    existing_tools.remove(tool_db.tool_name)
                except Exception as e:
                    continue
        for tool in existing_tools:
            # if tool.name == "REDDIT_SEARCH":
            payload = {
                "tool_name": tool,
                "uuid": get_uuid(),
                "app": tool,
                "status": True,
                "parameters": json.dumps(eval(f"ToolKit.{tool}.value[1]")),
                "meta_name": json.dumps(eval(f"ToolKit.{tool}.value[3]")),
            }
            ToolsController.create_tool(db, payload)

        logging.info("Added those tools in database. Update those tools accordigly")


class ToolsController:
    @staticmethod
    def create_tool(
        db: Session, tool_data: dict
    ) -> Tools:  # Not using this in current logic
        """
        Helper function to create a new tool with parameter validation.
        """
        if not validate_tool_parameters(tool_data.get("parameters", "{}")):
            raise ValueError("Invalid JSON in parameters field")

        tool = Tools(**tool_data)
        db.add(tool)
        db.commit()
        db.refresh(tool)
        return tool

    @staticmethod
    def update_tools(db: Session, id: str, payload: dict) -> Tools:
        tool = ToolsController.get_tool_by_uuid(db, id)
        payload.update({"updated_at": datetime.now()})
        # update provided fields
        for field, value in payload.items():
            if value is not None:
                setattr(tool, field, value)

        db.commit()
        db.refresh(tool)

        return tool

    @staticmethod
    def get_all_tools(db: Session) -> list[Tools]:
        tools = db.query(Tools).all()

        if tools:
            return tools
        else:
            return []

    @staticmethod
    def get_tool_by_uuid(db: Session, id: str) -> Tools:
        tool = db.query(Tools).filter(Tools.uuid == id).first()

        if tool:
            return tool

        raise HTTPException(detail="Tool not found", status_code=404)

    @staticmethod
    def get_tools_list_as_tool_instance(db: Session, tool_ids: list) -> tuple:
        tools = []
        # webhook_urls = []
        existing_tools = [tool_name.name for tool_name in ToolKit]

        for id in tool_ids:
            if id:
                tool = ToolsController.get_tool_by_uuid(db=db, id=id)
                tool_name = tool.tool_name
                # if tool.webhook_url:
                #     webhook_url = f"WEBHOOK URL OF {tool_name}: " + tool.webhook_url
                #     webhook_urls.append(webhook_url)

                if tool_name not in existing_tools:
                    raise HTTPException(
                        detail=f"Tool {tool_name} not found", status_code=404
                    )
                tools.append(eval(f"ToolKit.{tool_name}.value[0]"))
                # required_params = eval(f"ToolKit.{tool_name}.value[1]")

                # if required_params:
                #     keys = list(required_params.keys())

                #     for i in keys:
                #         var = f"{i} = {{{i}}},"
                #         params = params + var

        return tools  # , webhook_urls
