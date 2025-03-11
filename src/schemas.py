import datetime
import json

from pydantic import BaseModel, field_validator


class FieldUpdate(BaseModel):
    """Модель для хранения старого и нового значения поля."""

    old: str | int | list[str | int]
    new: str | int


class OperationDetails(BaseModel):
    """Модель деталей операции: изменение владельца или статуса."""

    owner: FieldUpdate | None = None
    status: FieldUpdate | None = None


class DocumentMeta(BaseModel):
    """Метаинформация о документе."""

    document_id: str
    document_type: str


class DocumentData(BaseModel):
    """Основные данные документа, включая объекты и детали операции."""

    document_data: DocumentMeta
    objects: list[str]
    operation_details: OperationDetails | None = None


class DocumentModel(BaseModel):
    """Полная модель документа, включая метаинформацию и статус обработки."""

    doc_id: str
    recieved_at: datetime.datetime
    document_type: str
    document_data: DocumentData
    processed_at: datetime.datetime | None = None

    @field_validator("document_data", mode="before")
    @classmethod
    def parse_json(cls, value):
        """Преобразует строку JSON в словарь, если это необходимо."""
        if isinstance(value, str):
            return json.loads(value)
        return value


class DataModel(BaseModel):
    """Модель объекта из таблицы data."""

    object: str
    owner: str
    status: int
    level: int
    parent: str | None = None
