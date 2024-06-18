from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, String


def StrEnumField(default, **kwargs):
    return Field(default=default, sa_column=Column(String), **kwargs)


def JsonbField(**kwargs):
    return Field(sa_column=Column(JSONB), **kwargs)
