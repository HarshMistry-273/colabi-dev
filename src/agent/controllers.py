from src.config import Config
from fastapi import HTTPException
from src.agent.models import Agent
from sqlalchemy.orm import Session
from src.utils.utils import get_uuid
from src.agent.task import embedding_docs


class AgentController:

    @staticmethod
    def get_agents_by_id_ctrl(db: Session, id: int) -> Agent:
        agent = db.query(Agent).filter(Agent.id == id).first()
        print("AGENT ID:",id)
        if agent:
            return agent

        raise HTTPException(detail="Agent not found", status_code=404)

    @staticmethod
    def update_agent_ctrl(
        db: Session,
        payload: dict = {},
    ) -> Agent:

        agent = AgentController.get_agents_by_id_ctrl(db=db, id=payload.get("id"))

        # Generate new namespace for vector store
        namespace = get_uuid()
        url_file_type = str(agent.own_data).rsplit(".")[-1]
        if url_file_type not in Config.SUPPORTED_FILE_TYPES:
            raise ValueError(
                f"Unsupported file type. Supported types: {Config.SUPPORTED_FILE_TYPES}"
            )
        # Schedule document embedding task
        embedding_docs.delay(
            api_key=Config.PINECONE_API_KEY,
            index_name=Config.PINECONE_INDEX_NAME,
            namespace=namespace,
            url=agent.own_data,
            url_file_type=url_file_type,
        )
        agent.vector_id = namespace

        db.commit()
        db.refresh(agent)

        return agent
