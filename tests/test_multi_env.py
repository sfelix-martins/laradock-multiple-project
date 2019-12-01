import unittest
import subprocess
import os
from mock import MagicMock

from multienv.database.database import Database
from multienv.database.dbms.mysql.mysql import MySQL
from multienv.docker_compose import DockerCompose
from multienv.exceptions import ProjectNotDefinedException, \
    ServicesNotDefinedException, InvalidYamlFileException, \
    ConfigFileNotFoundException, InvalidProjectDefinitions
from multienv.multi_env import MultiEnv
from multienv.config import Config
from multienv.web_servers.apache2.apache2 import Apache2
from multienv.web_servers.caddy.caddy import Caddy
from multienv.web_servers.nginx.nginx import Nginx


class MultiEnvTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures'

    def config(self, invalid=False, not_found_project=False):
        projects_file = 'ValidProjects.yml'
        if invalid:
            projects_file = 'InvalidProjects.yml'

        if not_found_project:
            projects_file = 'NotFound.yml'

        env_container = self.fixtures_folder + '/env_var_container_build.yml'

        return Config(
            dot_env=self.fixtures_folder + '/env',
            env_var_container_build=env_container,
            projects=self.fixtures_folder + '/' + projects_file,
            laradock_root_folder=self.fixtures_folder + '/laradock'
        )

    def define_config(self, project_definitions, env_definitions=None):
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

    def test_defined_project(self):
        multi_env = MultiEnv('site_1', self.config())

        self.assertEqual(multi_env.project_name, 'site_1')
        self.assertEqual(multi_env.project.get_name(), 'site_1')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['nginx', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

        # Assert defined the correct web server based on services
        self.assertIsInstance(multi_env.project.web_server, Nginx)

    def test_defined_project_with_apache2(self):
        multi_env = MultiEnv('site_apache2', self.config())

        self.assertEqual(multi_env.project_name, 'site_apache2')
        self.assertEqual(multi_env.project.get_name(), 'site_apache2')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['apache2', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

        # Assert defined the correct web server based on services
        self.assertIsInstance(multi_env.project.web_server, Apache2)

    def test_defined_project_with_caddy(self):
        multi_env = MultiEnv('site_caddy', self.config())

        self.assertEqual(multi_env.project_name, 'site_caddy')
        self.assertEqual(multi_env.project.get_name(), 'site_caddy')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['caddy', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

        # Assert defined the correct web server based on services
        self.assertIsInstance(multi_env.project.web_server, Caddy)

    def test_defined_project_without_server(self):
        multi_env = MultiEnv('site_without_server', self.config())

        self.assertEqual(multi_env.project_name, 'site_without_server')
        self.assertEqual(multi_env.project.get_name(), 'site_without_server')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['nginx', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

        # Assert defined the correct web server based on services
        self.assertEqual(multi_env.project.web_server, None)

    def test_defined_project_with_mysql(self):
        multi_env = MultiEnv('site_mysql', self.config())

        self.assertIsInstance(multi_env.project.dbms, MySQL)
        self.assertEqual(1, len(multi_env.project.get_databases()))
        for database in multi_env.project.get_databases():
            self.assertIsInstance(database, Database)

    def test_defined_project_with_mysql_two_databases(self):
        multi_env = MultiEnv('site_mysql_two_db', self.config())

        self.assertIsInstance(multi_env.project.dbms, MySQL)
        self.assertEqual(2, len(multi_env.project.get_databases()))
        for database in multi_env.project.get_databases():
            self.assertIsInstance(database, Database)

    def test_created_databases_files_mysql(self):
        multi_env = MultiEnv('site_mysql_two_db', self.config())
        multi_env.define_databases()

        # Assert exists createdb.sql file
        create_db_file = self.fixtures_folder + '/laradock/mysql' \
                                                '/docker-entrypoint-initdb.d' \
                                                '/site_mysql_two_db' \
                                                '/createdb.sql'

        self.assertTrue(os.path.isfile(create_db_file))

        os.remove(create_db_file)

    def test_defined_project_without_env_vars(self):
        multi_env = MultiEnv('site_without_env', self.config())

        self.assertEqual(multi_env.project_name, 'site_without_env')
        self.assertEqual(multi_env.project.get_name(), 'site_without_env')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['nginx', 'mysql'])

        self.assertEqual([], multi_env.project.env_vars)

        # Assert defined the correct web server based on services
        self.assertEqual(multi_env.project.web_server, None)

    def test_defined_project_with_more_than_one_server_service(self):
        with self.assertRaises(InvalidProjectDefinitions):
            MultiEnv('site_with_more_than_one_server', self.config())

    def test_defined_project_with_invalid_server(self):
        with self.assertRaises(InvalidProjectDefinitions):
            MultiEnv('site_with_wrong_server', self.config())

    def test_env_var_was_changed(self):
        # Define vars to .env file
        initial_value = str(5.6)
        subprocess.call(
            ["sed -i.bak '/^PHP_VERSION/s/=.*$/="
             + initial_value + "/' " + self.fixtures_folder + "/env"],
            shell=True
        )

        env_var_before_test = subprocess.check_output(
            ["grep PHP_VERSION " + self.fixtures_folder +
             "/env | awk -F= '{print $2}'"],
            shell=True
        ).decode('utf-8')

        self.assertEqual(initial_value, env_var_before_test.strip())

        multi_env = MultiEnv('site_1', self.config())
        multi_env.define_env()

        env_var = subprocess.check_output(
            ["grep PHP_VERSION " + self.fixtures_folder +
             "/env | awk -F= '{print $2}'"],
            shell=True
        ).decode('utf-8')

        self.assertEqual(str(7.2), env_var.strip())

    def test_up(self):
        docker_compose = DockerCompose()
        docker_compose.down = MagicMock()
        docker_compose.build = MagicMock()
        docker_compose.up = MagicMock()

        multi_env = MultiEnv('site_1',
                             self.config(),
                             docker_compose=docker_compose)
        self.assertTrue(multi_env.up())

    def test_up_with_databases_to_create_and_exists_data_folder_for_mysql(self):
        data_path_host = self.fixtures_folder + '/.laradock/data'

        if not os.path.exists(data_path_host):
            os.makedirs(data_path_host)

        env = """
DATA_PATH_HOST=""" + data_path_host + """
MYSQL_USER=default
"""
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
        config = self.define_config(project, env)

        docker_compose = DockerCompose()
        docker_compose.down = MagicMock()
        docker_compose.build = MagicMock()
        docker_compose.up = MagicMock()

        multi_env = MultiEnv('app', config, docker_compose)
        multi_env.up()

        with open(config.dot_env_file(), 'r') as file:
            dot_env_file_content = file.read()

            self.assertTrue(
                'DATA_PATH_HOST=~/.laradock/data/app' in dot_env_file_content)
            self.assertTrue(
                'MYSQL_ENTRYPOINT_INITDB=./mysql/docker-entrypoint-initdb.d/app'
                in dot_env_file_content)

        os.rmdir(data_path_host)

    def test_exec(self):
        docker_compose = DockerCompose()
        docker_compose.execute = MagicMock()

        multi_env = MultiEnv('site_1',
                             self.config(),
                             docker_compose=docker_compose)
        self.assertTrue(multi_env.execute())

    def test_create_multi_env_with_config_invalid(self):
        with self.assertRaises(TypeError):
            MultiEnv('not_existent_project', config='test')

    def test_create_multi_env_with_docker_compose_invalid(self):
        with self.assertRaises(TypeError):
            MultiEnv('not_existent_project',
                     self.config(),
                     docker_compose='test')

    def test_define_projects_with_not_existent_project(self):
        with self.assertRaises(ProjectNotDefinedException):
            MultiEnv('not_existent_project', self.config()).define_project()

    def test_define_projects_without_services_defined(self):
        with self.assertRaises(ServicesNotDefinedException):
            MultiEnv('site_without_services', self.config())

    def test_define_projects_with_invalid_project_definitions_yaml_file(self):
        with self.assertRaises(InvalidYamlFileException):
            MultiEnv('site_1', self.config(invalid=True))

    def test_define_projects_with_not_existent_config_file(self):
        with self.assertRaises(ConfigFileNotFoundException):
            MultiEnv('site_without_services',
                     self.config(not_found_project=True))

    def test_define_web_server_without_web_server_defined(self):
        multi_env = MultiEnv('site_without_server_service', self.config())
        self.assertIsNone(multi_env.define_web_server())


if __name__ == '__main__':
    unittest.main()
