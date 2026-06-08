from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid6
from typing import Optional


"""
Vou simular a tabela que precisaria registrar as tentativas de envio para o SAP.
 Se o SAP falhar, o status fica como PENDING para o mecanismo de retry processar depois.
"""

class SAPIntegrationLog(SQLModel, table=True):
    __tablename__ = "sap_integration_logs"

    # No momento da inserção irá gerar o UUIDv7 ordenado por tempo
    id: str = Field(
        default_factory=lambda: str(uuid6.uuid7()),
        primary_key=True,
        description="UUIDv7 ordenado por tempo - Otimizado para B-Tree"
    )
    contract_ref: str = Field(index=True, description="ID do contrato na Clicksign")
    customer_id: str
    amount: float
    status: str = Field(default="PENDING", description="PENDING, SUCCESS, FAILED")
    sap_document_number: Optional[str] = Field(default=None)
    attempts: int = Field(default=0)
    last_attempt: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = Field(default=None)