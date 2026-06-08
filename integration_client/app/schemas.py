from pydantic import BaseModel, Field


"""
Esse é o payload que o Middleware vai receber 
pense no webhook avisando que um contrato foi assinado.

"""


class ContractSignedWebhook(BaseModel):
    contract_ref: str = Field(..., description="ID do contrato assinado")
    customer_id: str = Field(..., description="ID do cliente relacionado")
    amount: float = Field(..., gt=0, description="Valor do faturamento")
    company_code: str = Field("BR01", max_length=4, max_digits=4)

    class Config:
        json_schema_extra = {
            "example": {
                "contract_ref": "c4b1a829-9dc4-4d1a-8533-87a1122a2026",
                "customer_id": "CUST-9901",
                "amount": 1500.50,
                "company_code": "BR01"
            }
        }