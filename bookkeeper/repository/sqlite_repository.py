"""
Module for repository working with sqlite3 database
"""

from typing import Any
from inspect import get_annotations

from pony import orm

from bookkeeper.repository.abstract_repository import AbstractRepository, T
import bookkeeper.repository.databases as my_dbs
from bookkeeper.utils import py2sqlite_type_converter


class SQLiteRepository(AbstractRepository[T]):
    """
    SQLite3 repository
    """
    def __init__(self, data_cls: type,
                 table_name: str) -> None:

        self.table_cls = my_dbs.DatabaseHelper.get_table_by_name(table_name)
        self.data_cls = data_cls
        self.data_cls_fields = get_annotations(self.data_cls, eval_str=True)
        self.data_cls_fields.pop('pk')

    @staticmethod
    def bind_database(db_filename: str = 'database.db') -> None:
        """ Bind database to db in file <db_filename> """
        my_dbs.db.bind(provider='sqlite',
                       filename=db_filename,
                       create_db=True)

        my_dbs.db.generate_mapping(create_tables=True)

    @orm.db_session
    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')

        kwargs = {
            f: py2sqlite_type_converter(getattr(obj, f))
            for f in self.data_cls_fields.keys()
        }
        db_obj = self.table_cls(**kwargs)
        orm.commit()

        obj.pk = db_obj.pk
        return obj.pk

    @orm.db_session
    def get(self, pk: int) -> T | None:
        try:
            db_obj = self.table_cls[pk]
            return self.data_cls(**db_obj.get_data())

        except orm.ObjectNotFound:
            return None

    @orm.db_session
    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        db_obj = self.table_cls[obj.pk]

        for field in self.data_cls_fields.keys():
            setattr(db_obj, field, py2sqlite_type_converter(getattr(obj, field)))

    @orm.db_session
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:

        if where is None:  # return all objects from the table
            db_objs_lst = orm.select(p for p in self.table_cls)[:]

            objs_lst = []
            for db_obj in db_objs_lst:
                objs_lst.append(self.data_cls(**db_obj.get_data()))

            return objs_lst

        # return objects accroding to condition
        attr1, value1 = list(where.items())[0]  # first condition
        # can not put all conditions inside a query, so use at least one condition
        db_objs_lst = orm.select(p for p in self.table_cls
                                 if getattr(p, attr1) == value1)[:]
        # apply all conditions
        db_objs_lst = [p for p in db_objs_lst
                       if all(getattr(p, attr) == value
                              for (attr, value) in where.items())]

        objs_lst = []
        for db_obj in db_objs_lst:
            objs_lst.append(self.data_cls(**db_obj.get_data()))

        return objs_lst

    @orm.db_session
    def delete(self, pk: int) -> None:
        try:
            self.table_cls[pk].delete()
        except orm.ObjectNotFound:
            pass
