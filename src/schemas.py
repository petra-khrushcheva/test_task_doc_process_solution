import json
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


class FieldUpdate(BaseModel):
    """Модель для хранения старого и нового значения поля."""

    old: Union[str, int, List[Union[str, int]]]
    new: Union[str, int]


class OperationDetails(BaseModel):
    """Модель деталей операции: изменение владельца или статуса."""

    owner: Optional[FieldUpdate] = None
    status: Optional[FieldUpdate] = None


class DocumentMeta(BaseModel):
    """Метаинформация о документе."""

    document_id: str
    document_type: str


class DocumentData(BaseModel):
    """Основные данные документа, включая объекты и детали операции."""

    document_data: DocumentMeta
    objects: List[str]
    operation_details: Optional[OperationDetails] = None


class DocumentModel(BaseModel):
    """Полная модель документа, включая метаинформацию и статус обработки."""

    doc_id: str
    recieved_at: str
    document_type: str
    document_data: DocumentData
    processed_at: Optional[str] = None

    @field_validator("document_data", mode="before")
    @classmethod
    def parse_json(cls, value):
        """Преобразует строку JSON в словарь, если это необходимо."""
        if isinstance(value, str):
            return json.loads(value)
        return value


# ✅ Используем asyncio.run(main()), чтобы запустить код.
