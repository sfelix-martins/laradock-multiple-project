from multienv.database.dbms.dbms import DBMS
from multienv.database.dbms.mysql.mysql import MySQL
from multienv.exceptions import InvalidArgumentException


class DBMSFactory:
    name = None

    def __init__(self, name: str):
        if name not in DBMS.available_dbms:
            raise InvalidArgumentException(
                error='DBMS [' + name + '] not found',
                hint='You must choose one of these: ['
                     + ', '.join(DBMS.available_dbms) + ']'
            )

        self.name = name

    def create(self, laradock_root_folder: str) -> DBMS:
        """
        Create an instance of the DBMS from name.

        :param laradock_root_folder:
        :return: DBMS
        :raises: NotImplementedError
        """
        if self.name == 'mysql':
            return MySQL(laradock_root_folder)

        raise NotImplementedError()
