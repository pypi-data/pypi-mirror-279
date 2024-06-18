from pydantic import ConfigDict

from sqlmako.queryset import ObjectModel


class SQLMako(ObjectModel):
    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)
