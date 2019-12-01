import os

from multienv.database.dbms.dbms import DBMS
from multienv.project.project import Project


class MySQL(DBMS):
    user_attribute: str = 'MYSQL_USER'

    def create_databases(self, project: Project):
        sql_folder = self.__get_sql_folder(project)
        if not os.path.exists(sql_folder):
            os.makedirs(sql_folder)

        sql_file = f'{sql_folder}/createdb.sql'

        for db in project.get_databases():
            create_db_sql = """
CREATE DATABASE IF NOT EXISTS `""" + db.name + """` COLLATE 'utf8_general_ci' ;
GRANT ALL ON `""" + db.name + """`.* TO 'default'@'%' ;

"""

            with open(sql_file, 'a+') as file:
                file.write(create_db_sql)

        flush_privileges = 'FLUSH PRIVILEGES'

        has_flush = False
        if os.path.isfile(sql_file):
            has_flush = flush_privileges in open(sql_file, 'r').read()
        if not has_flush:
            with open(sql_file, 'a') as file:
                file.write(f'{flush_privileges} ;')

    def __get_sql_folder(self, project: Project) -> str:
        """
        Get the sql file name that will be filled.

        :param project:
        :return:
        """
        return f'{self.laradock_root_folder}' \
               f'/mysql/docker-entrypoint-initdb.d' \
               f'/{project.get_name()}'
