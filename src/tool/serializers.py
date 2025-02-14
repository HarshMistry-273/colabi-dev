from typing import Optional
from src.tool.models import Tools
from pydantic import BaseModel


class CreateToolSchema(BaseModel):
    tool_name: str
    app: str
    action: str


class UpdateToolSchema(BaseModel):
    apps: Optional[str] = None
    actions: Optional[str] = None
    parameters: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = None


def get_tools_serializer(tools: list[Tools]) -> list[dict]:
    tools_list = []

    if not isinstance(tools, list):
        tools = [tools]
    for tool in tools:
        tool_dict = {
            # Primary Key
            "id": tool.id,
            "uuid": tool.uuid,
            # Tool Information
            "tool_name": tool.tool_name,
            "app": tool.app,
            "action": tool.action if tool.action else "",
            "webhook_url": tool.webhook_url if tool.webhook_url else "",
            # # Parameters as parsed JSON
            "parameters": tool.parameters if tool.parameters else "",
            # # Additional Information
            "description": tool.description,
            "status": tool.status,
            "status_text": "active" if tool.status else "inactive",
            "meta_data": tool.meta_data if tool.meta_data else "",
            # # Timestamps
            "created_at": str(tool.created_at),
            "updated_at": str(tool.updated_at),
        }
        tools_list.append(tool_dict)

    return tools_list
