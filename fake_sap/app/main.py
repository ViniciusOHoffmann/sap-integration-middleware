from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uuid6
import random

app = FastAPI(
    title="Fake SAP ERP Server",
    description="Simulador de endpoint SAP (Módulos FI/SD) para testes de integração"
)

# Aqui será o Schema que simulará o formato rígido que o SAP exige para faturamento
class SAPInvoicePayload(BaseModel):
    company_code: str = Field(..., min_length=4, max_length=4, description="Ex: BR01")
    customer_id: str = Field(...,description="ID do Cliente no SAP")
    amount: float = Field(..., gt=0)
    contract_ref: str = Field(..., description="UUID do contrato Clicksign")

@app.post("/sap/api/v1/accounting/invoices", status_code=status.HTTP_201_CREATED)
def create_sap_invoice(payload: SAPInvoicePayload):
    """
    Irá Simular o comportamento de uma BAPI de Faturamento no SAP.
    Possui uma chance intencional de falha, 500, para testar a resiliência do cliente.
    """
    
    # Simulação de instabilidade randômica do SAP (Legados costuman falhar ou ficar lentos)
    if random.choice([True, False, False]): # 33% de chance de simular o SAP ficar fora do ar
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SAP RFC connection Timeout: System Overloaded"
        )
    
    # Cenário de sucesso: Retorna estruturas típicas do padrão SAP
    sap_document_id = f"DOC-SAP-{random.randint(100000, 999999)}"
    
    return {
        "status": "SUCCESS",
        "sap_document_number": sap_document_id,
        "contract_reference": payload.contract_ref,
        "message": f"Invoice posted successfully in Company Code {payload.company_code}."
    }

