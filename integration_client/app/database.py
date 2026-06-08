from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os

# Busca a string que eu coloquei no arquivo .env, caso ele não encontrar, usa-se um fallback local
RAW_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/clicksign_sap"
)

# Adptação necessária para o driver assíncrono Psycopg 3 para funcionar com a Neon
if RAW_DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)
else:
    DATABASE_URL = RAW_DATABASE_URL

# Criei uma engine e passei um connect_args para garantir suporte ao SSL da Neon
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"sslmode": "require"} if "neon.tech" in DATABASE_URL else {}
)

async def init_db():
    async with async_engine.begin() as conn:
        from .models import SAPIntegrationLog
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session