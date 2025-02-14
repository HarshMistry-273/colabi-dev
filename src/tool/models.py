from database import Base
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, JSON


class Tools(Base):
    __tablename__ = "tools"

    # Primary Key
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    # Tool Information
    tool_name = Column(String(255, collation="utf8mb4_unicode_ci"), nullable=False)
    app = Column(String(255, collation="utf8mb4_unicode_ci"), nullable=False)
    action = Column(String(255, collation="utf8mb4_unicode_ci"), nullable=True)
    webhook_url = Column(String(255, collation="utf8mb4_unicode_ci"), nullable=True)

    # JSON Parameters with validation
    parameters = Column(JSON, nullable=True)

    # Additional Information
    description = Column(String(255, collation="utf8mb4_unicode_ci"), nullable=True)
    status = Column(Boolean, nullable=False)

    # Timestamps
    meta_data = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # @property
    # def parameters_json(self) -> Dict[str, Any]:
    #     """
    #     Returns the parameters as a Python dictionary.
    #     Handles JSON validation internally.
    #     """
    #     try:
    #         return json.loads(self.parameters)
    #     except json.JSONDecodeError:
    #         return {}
