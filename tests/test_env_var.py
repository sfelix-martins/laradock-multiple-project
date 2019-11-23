import unittest

from multienv.config import Config
from multienv.env_var import EnvVar
from multienv.exceptions import InvalidYamlFileException, \
    EnvVarContainerBuildNotFoundException


class EnvVarTestCase(unittest.TestCase):
    def test_get_containers_to_rebuild_with_existent_env_var(self):
        config = Config(
            env_var_container_build='tests/fixtures/'
                                    'env_var_container_build.yml')
        env_var = EnvVar('PHP_VERSION', 7.1, config)
        self.assertEqual(
            env_var.get_containers_to_rebuild(),
            ['php-fpm', 'workspace']
        )

    def test_get_containers_to_rebuild_with_not_exists_env_var(self):
        config = Config(
            env_var_container_build='tests/fixtures/'
                                    'env_var_container_build.yml')
        env_var = EnvVar('MYSQL_VERSION', 5.7, config)
        self.assertEqual(env_var.get_containers_to_rebuild(), [])

    def test_get_containers_to_rebuild_with_invalid_config(self):
        with self.assertRaises(InvalidYamlFileException):
            config = Config(
                env_var_container_build='tests/fixtures'
                                        '/invalid_env_var_container_build.yml')
            env_var = EnvVar('MYSQL_VERSION', 5.7, config)
            env_var.get_containers_to_rebuild()

    def test_get_containers_to_rebuild_with_not_existent_config(self):
        with self.assertRaises(EnvVarContainerBuildNotFoundException):
            config = Config(
                env_var_container_build='not_found/'
                                        'env_var_container_build.yml')
            env_var = EnvVar('MYSQL_VERSION', 5.7, config)
            env_var.get_containers_to_rebuild()


if __name__ == '__main__':
    unittest.main()
