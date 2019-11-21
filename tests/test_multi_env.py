import unittest
import subprocess
import os
from mock import MagicMock

from multienv.docker_compose import DockerCompose
from multienv.exceptions import ProjectNotDefinedException, \
    ServicesNotDefinedException, InvalidYamlFileException, \
    ConfigFileNotFoundException
from multienv.multi_env import MultiEnv
from multienv.config import Config


class MultiEnvTestCase(unittest.TestCase):

    def test_defined_project(self):
        config = Config(
            dot_env='tests/fixtures/.env_',
            env_var_container_build='tests/fixtures/'
                                    'env_var_container_build.yml',
            projects='tests/fixtures/ValidProjects.yml'
        )

        multi_env = MultiEnv('site_1', config)

        self.assertEqual(multi_env.project_name, 'site_1')
        self.assertEqual(multi_env.project.name, 'site_1')

        for service in multi_env.project.services:
            self.assertIn(service.name, ['nginx', 'mysql', 'mailhog'])

        for env in multi_env.project.env_vars:
            self.assertEqual(env.name, 'PHP_VERSION')
            self.assertEqual(env.value, str(7.2))

    def test_env_var_was_changed(self):
        # Define vars to .env file
        initial_value = str(5.6)
        subprocess.call(
            ["sed -i .bak '/^PHP_VERSION/s/=.*$/="
             + initial_value + "/' tests/fixtures/.env_"],
            shell=True
        )

        env_var_before_test = subprocess.check_output(
            ["grep PHP_VERSION tests/fixtures/.env_ | awk -F= '{print $2}'"],
            shell=True
        ).decode('utf-8')

        self.assertEqual(initial_value, env_var_before_test.strip())

        config = Config(
            dot_env='tests/fixtures/.env_',
            env_var_container_build='tests/fixtures/'
                                    'env_var_container_build.yml',
            projects='tests/fixtures/ValidProjects.yml'
        )

        multi_env = MultiEnv('site_1', config)
        multi_env.define_env()

        env_var = subprocess.check_output(
            ["grep PHP_VERSION tests/fixtures/.env_ "
             "| awk -F= '{print $2}'"],
            shell=True
        ).decode('utf-8')

        self.assertEqual(str(7.2), env_var.strip())

        # Assert created backup file with previous .env vars
        self.assertTrue(os.path.isfile('tests/fixtures/.env_.bak'))

        env_var_bak_file = subprocess.check_output(
            ["grep PHP_VERSION tests/fixtures/.env_.bak "
             "| awk -F= '{print $2}'"],
            shell=True
        ).decode('utf-8')

        self.assertEqual(initial_value, env_var_bak_file.strip())

    def test_up(self):
        docker_compose = DockerCompose()
        docker_compose.down = MagicMock()
        docker_compose.build = MagicMock()
        docker_compose.up = MagicMock()

        config = Config(
            dot_env='tests/fixtures/.env_',
            env_var_container_build='tests/fixtures/'
                                    'env_var_container_build.yml',
            projects='tests/fixtures/ValidProjects.yml'
        )

        multi_env = MultiEnv('site_1', config, docker_compose=docker_compose)
        self.assertTrue(multi_env.up())

    def test_create_multi_env_with_config_invalid(self):
        with self.assertRaises(TypeError):
            MultiEnv('not_existent_project', config='test')

    def test_create_multi_env_with_docker_compose_invalid(self):
        with self.assertRaises(TypeError):
            config = Config(
                dot_env='tests/fixtures/.env_',
                env_var_container_build='tests/fixtures'
                                        '/env_var_container_build.yml',
                projects='tests/fixtures/ValidProjects.yml'
            )

            MultiEnv('not_existent_project', config, docker_compose='test')

    def test_define_projects_with_not_existent_project(self):
        with self.assertRaises(ProjectNotDefinedException):
            config = Config(
                dot_env='tests/fixtures/.env_',
                env_var_container_build='tests/fixtures'
                                        '/env_var_container_build.yml',
                projects='tests/fixtures/ValidProjects.yml'
            )

            env = MultiEnv('not_existent_project', config)
            a = env.define_project()

            print(a)

    def test_define_projects_without_services_defined(self):
        with self.assertRaises(ServicesNotDefinedException):
            config = Config(
                dot_env='tests/fixtures/.env_',
                env_var_container_build='tests/fixtures'
                                        '/env_var_container_build.yml',
                projects='tests/fixtures/ValidProjects.yml'
            )

            MultiEnv('site_without_services', config)

    def test_define_projects_with_invalid_project_definitions_yaml_file(self):
        with self.assertRaises(InvalidYamlFileException):
            config = Config(
                dot_env='tests/fixtures/.env_',
                env_var_container_build='tests/fixtures'
                                        '/env_var_container_build.yml',
                projects='tests/fixtures/InvalidProjects.yml'
            )

            MultiEnv('site_without_services', config)

    def test_define_projects_with_not_existent_config_file(self):
        with self.assertRaises(ConfigFileNotFoundException):
            config = Config(
                dot_env='tests/fixtures/.env_',
                env_var_container_build='tests/fixtures'
                                        '/env_var_container_build.yml',
                projects='tests/fixtures/not_exists/ValidProjects.yml'
            )

            MultiEnv('site_without_services', config)


if __name__ == '__main__':
    unittest.main()
