import abc
from typing import List


class DBMS:
    user_attribute: str = 'default'
    laradock_root_folder: str
    available_dbms: List[str] = [
        'mysql',
        'postgres',
    ]

    def __init__(self, laradock_root_folder: str = '..'):
        self.laradock_root_folder = laradock_root_folder

    @abc.abstractmethod
    def create_databases(self, databases):
        pass
