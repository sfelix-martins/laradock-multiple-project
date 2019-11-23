import unittest
import subprocess
from mock import MagicMock

from multienv.docker_compose import DockerCompose
from multienv.exceptions import ProjectNotDefinedException, \
    ServicesNotDefinedException, InvalidYamlFileException, \
    ConfigFileNotFoundException, InvalidProjectDefinitions
from multienv.multi_env import MultiEnv
from multienv.config import Config
from multienv.webservers.nginx.nginx import Nginx


class MultiEnvTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures'

    def config(self, invalid=False, not_found_project=False):
        projects_file = 'ValidProjects.yml'
        if invalid:
            projects_file = 'InvalidProjects.yml'

        if not_found_project:
            projects_file = 'NotFound.yml'

        return Config(
            dot_env=self.fixtures_folder + '/env',
            env_var_container_build=
            self.fixtures_folder + '/env_var_container_build.yml',
            projects=self.fixtures_folder + '/' + projects_file,
            laradock_root_folder=self.fixtures_folder + '/laradock'
        )

    def test_defined_project(self):
        multi_env = MultiEnv('site_1', self.config())

        self.assertEqual(multi_env.project_name, 'site_1')
        self.assertEqual(multi_env.project.name, 'site_1')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['nginx', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

        # Assert defined the correct web server based on services
        self.assertIsInstance(multi_env.project.web_server, Nginx)

    def test_defined_project_without_server(self):
        multi_env = MultiEnv('site_without_server', self.config())

        self.assertEqual(multi_env.project_name, 'site_without_server')
        self.assertEqual(multi_env.project.name, 'site_without_server')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['nginx', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

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
            MultiEnv('not_existent_project', self.config(), docker_compose='test')

    def test_define_projects_with_not_existent_project(self):
        with self.assertRaises(ProjectNotDefinedException):
            MultiEnv('not_existent_project', self.config()).define_project()

    def test_define_projects_without_services_defined(self):
        with self.assertRaises(ServicesNotDefinedException):
            MultiEnv('site_without_services', self.config())

    def test_define_projects_with_invalid_project_definitions_yaml_file(self):
        with self.assertRaises(InvalidYamlFileException):
            MultiEnv('site_without_services', self.config(invalid=True))

    def test_define_projects_with_not_existent_config_file(self):
        with self.assertRaises(ConfigFileNotFoundException):
            MultiEnv('site_without_services', self.config(not_found_project=True))


if __name__ == '__main__':
    unittest.main()
