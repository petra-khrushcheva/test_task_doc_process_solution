import datetime
import logging

import asyncpg

from schemas import DataModel, DocumentModel, FieldUpdate, OperationDetails


async def get_unprocessed_document(
    conn: asyncpg.Connection,
) -> DocumentModel | None:
    """Находит первый необработанный документ с типом transfer_document."""
    query = """
    SELECT * FROM documents
    WHERE document_type = 'transfer_document' AND processed_at IS NULL
    ORDER BY recieved_at ASC
    LIMIT 1;
    """
    row = await conn.fetchrow(query)
    return DocumentModel(**dict(row)) if row else None


async def get_related_objects(
    conn: asyncpg.Connection, parent_ids: list[str]
) -> list[DataModel]:
    """
    Принимает список ID родительских объектов, возвращает список
    родительских и связанных с ними дочерних объектов.
    """
    query = """
    SELECT * FROM data
    WHERE object = ANY($1) OR parent = ANY($1);
    """
    rows = await conn.fetch(query, parent_ids)
    return [DataModel(**dict(row)) for row in rows]


async def update_objects(
    conn: asyncpg.Connection,
    objects: list[DataModel],
    operation_details: OperationDetails | None,
):
    """
    Обновляет объекты в таблице data, если все `old` значения
    из operation_details совпадают с данными обьектов бд.
    """

    if not operation_details:
        logging.info("Нет данных для обновления.")
        return

    matched_objects_ids = []

    for obj in objects:
        for field, update_data in operation_details.__dict__.items():
            if update_data is None:
                continue

            update_data: FieldUpdate = update_data
            obj_value = getattr(obj, field)

            if isinstance(update_data.old, list):
                if obj_value not in update_data.old:
                    break
            else:
                if obj_value != update_data.old:
                    break
        else:
            matched_objects_ids.append(obj.object)

    if not matched_objects_ids:
        logging.info(
            "Не найдено ни одного объекта, у которого все текущие значения "
            "совпадают с ключами old из operation_details"
        )
        return

    set_clauses = []
    values = []

    fields = [
        field
        for field in operation_details.__dict__
        if getattr(operation_details, field)
    ]

    for i, field in enumerate(fields):
        update_data = getattr(operation_details, field)
        set_clauses.append(f"{field} = ${i+1}")
        values.append(update_data.new)

    query = f"""
        UPDATE data
        SET {", ".join(set_clauses)}
        WHERE object = ANY(${len(values) + 1});
    """

    values.append(matched_objects_ids)

    await conn.execute(query, *values)

    logging.info(f"Успешно обновлено {len(matched_objects_ids)} объектов.")


async def mark_document_processed(conn: asyncpg.Connection, doc_id: str):
    """Помечает документ как обработанный."""
    query = "UPDATE documents SET processed_at = $1 WHERE doc_id = $2;"
    await conn.execute(query, datetime.datetime.now(), doc_id)


async def process_document(db_config: dict[str, str]) -> bool:
    """Основная логика обработки документа."""
    try:
        pool = await asyncpg.create_pool(**db_config)

        async with pool.acquire() as conn:
            async with conn.transaction():
                doc = await get_unprocessed_document(conn)
                if not doc:
                    logging.info("Нет документов для обработки.")
                    return True

                object_ids = doc.document_data.objects
                operation_details = doc.document_data.operation_details

                all_objects = await get_related_objects(
                    conn, parent_ids=object_ids
                )

                await update_objects(conn, all_objects, operation_details)

                await mark_document_processed(conn, doc.doc_id)

                logging.info(f"Документ {doc.doc_id} обработан.")
                return True

    except Exception:
        logging.exception("Ошибка при обработке документа: ")
        return False
