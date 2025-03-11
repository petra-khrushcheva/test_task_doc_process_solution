import asyncio

from config import Settings
from doc_process import process_document
from log_config import configure_logging


async def main():
    settings = Settings()
    configure_logging(log_config=settings.log_config)
    await process_document(db_config=settings.asyncpg_database_config)


if __name__ == "__main__":
    asyncio.run(main())
