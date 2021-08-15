from abc import ABC, abstractmethod
import sqlite3 as sl


class Dao(ABC):

    db_name = 'sdx_db.db'

    @abstractmethod
    def get_by_id(self, obj_id):
        pass

    @abstractmethod
    def create(self, obj):
        pass

    @abstractmethod
    def get_obj_from_result(self):
        pass

    @staticmethod
    def get_db_conn():
        return sl.connect(Dao.db_name)
