from pydantic import BaseModel


class OutputFile(BaseModel):
    topic: list[str]
    summary: list[str]
    link: list[str] = None
