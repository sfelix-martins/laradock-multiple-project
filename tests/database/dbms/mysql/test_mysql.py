import unittest
import os
from unittest.mock import Mock, MagicMock

from multienv.database.database import Database
from multienv.database.dbms.mysql.mysql import MySQL


class MySqlTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures'

    def test_create_databases_file(self):
        project_name = 'test_project'
        project = Mock()
        project.get_name = MagicMock(return_value=project_name)
        databases = [Database(name='test'), Database(name='laradock')]
        project.get_databases = MagicMock(return_value=databases)

        db = MySQL(self.fixtures_folder + '/laradock')
        db.create_databases(project)

        # Assert exists createdb.sql file
        create_db_file = f'{self.fixtures_folder}/laradock/mysql' \
                         f'/docker-entrypoint-initdb.d/{project_name}' \
                         f'/createdb.sql'

        self.assertTrue(os.path.isfile(create_db_file))

        # Assert content of the file
        db_creation = "CREATE DATABASE IF NOT EXISTS `test` COLLATE " \
                      "'utf8_general_ci' ;"
        grant_permission = "GRANT ALL ON `test`.* TO 'default'@'%' ;"

        file = open(create_db_file, 'r')
        file_content = file.read()

        self.assertTrue(db_creation in file_content)
        self.assertTrue(grant_permission in file_content)

        # Assert content of the file to database `laradock`
        db_creation = "CREATE DATABASE IF NOT EXISTS `laradock` COLLATE " \
                      "'utf8_general_ci' ;"
        grant_permission = "GRANT ALL ON `laradock`.* TO 'default'@'%' ;"

        file = open(create_db_file, 'r')
        file_content = file.read()

        self.assertTrue(db_creation in file_content)
        self.assertTrue(grant_permission in file_content)

        # Assert flush privileges just one time
        flush_privileges = 'FLUSH PRIVILEGES ;'

        # Assert has just one flush privileges string
        flush_privileges_amount = sum(1 for line in open(create_db_file)
                                      if flush_privileges in line)

        self.assertEqual(1, flush_privileges_amount)

        # Assert flush privileges on last line
        with open(create_db_file, 'r') as f:
            lines = f.read().strip().splitlines()
            last_line = lines[-1]

            self.assertTrue(flush_privileges in last_line)

        # Removed createdb.sql file
        os.remove(create_db_file)


if __name__ == '__main__':
    unittest.main()
