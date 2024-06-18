"""This module is meant to help you create tables or two-dimensional data structures"""

import numpy as np
from typing import Any, Self
from enum import (Enum, auto)

class AccessDenied(TypeError):
    def __init__(self, *message: str):
        raise super(TypeError).__init__(*message)

class ColumnTypes(Enum):
    automatic_id = auto()
    string = auto()
    integer = auto()
    Real = auto()

class Column:
    def __init__(self, name: str, kind: ColumnTypes):
        self.name = name
        self.kind = kind
        self.type = kind

class Matrix:
    def __init__(self, *columns: Column):
        self.main_column = Column('ID', kind = ColumnTypes.automatic_id)
        self.mc = self.main_column
        self.columns: list[Column] = list(columns)
        self.data: dict[int, dict[str, Any]] = {}

    def add_column(self, *columns: Column) -> Self:
        try:
            for i in columns:
                if i.type == ColumnTypes.automatic_id:
                    raise AccessDenied(f"Only the default column of a Matrix can have an `automatic_id` column, not `{i.name}`!")

            self.columns.extend(list(columns))

            for ID, item in self.data.items():
                if not self.data:
                    return
                for column in columns:
                    if column.type == ColumnTypes.Real:
                        item[column.name] = 0.0
                    elif column.type == ColumnTypes.string:
                        item[column.name] = ''
                    elif column.type == ColumnTypes.integer:
                        item[column.name] = 0

        finally:
            return self

    def add_row(self, **data) -> Self:
        toAdd: dict[str, Any] = {}
        for k, v in data.items():
            if k not in self.columns:
                raise IndexError()
            toAdd[k] = v
        self.data[int(max(list(self.data.keys())))] = toAdd
        return self

    def __repr__(self) -> np.array:
        DATA: list = [column.name for column in self.columns]
        for ID, value in self.data.items():
            ToAdd = [ID]
            for _, v in value.items():
                ToAdd.append(v)
            DATA.extend(ToAdd)
        return np.array(DATA)
