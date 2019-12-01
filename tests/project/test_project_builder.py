import unittest

from multienv.config import Config
from multienv.database.database import Database
from multienv.project.project_builder import ProjectBuilder


class ProjectBuilderTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures'

    def config(self, project_definitions, env_definitions=None):
        projects_file = self.fixtures_folder + '/Projects.yml'
        with open(projects_file, 'w') as file:
            file.write(project_definitions)

        env_file = self.fixtures_folder + '/env'
        if env_definitions:
            env_file = self.fixtures_folder + '/env_file'
            with open(env_file, 'w') as file:
                file.write(env_definitions)

        env_container = self.fixtures_folder + '/env_var_container_build.yml'

        return Config(
            dot_env=env_file,
            env_var_container_build=env_container,
            projects=projects_file,
            laradock_root_folder=self.fixtures_folder + '/laradock')

    def test_defined_databases_with_user_from_env_vars_mysql(self):
        project = """
app:
  env:
    - MYSQL_USER: 'smartins'
  services:
    - mysql
  databases:
    - app
    - app_test
"""

        env = """
PHP_VERSION=5.6
MYSQL_USER=smartins        
"""
        built = ProjectBuilder('app', self.config(project, env))

        for db in built.project.get_databases():
            self.assertIsInstance(db, Database)
            self.assertEqual('smartins', db.user)

        self.assertEqual('app', built.project.get_databases()[0].name)
        self.assertEqual('app_test', built.project.get_databases()[1].name)

    def test_defined_databases_without_user_from_env_vars_mysql(self):
        project = """
app:
  env:
    - MYSQL_USER: 'smartins'
  services:
    - mysql
  databases:
    - app
    - app_test
"""

        env = """
PHP_VERSION=5.6  
"""
        built = ProjectBuilder('app', self.config(project, env))

        for db in built.project.get_databases():
            self.assertIsInstance(db, Database)
            self.assertEqual('default', db.user)

        self.assertEqual('app', built.project.get_databases()[0].name)
        self.assertEqual('app_test', built.project.get_databases()[1].name)


if __name__ == '__main__':
    unittest.main()
