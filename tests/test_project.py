import unittest

from multienv.config import Config
from multienv.env_var import EnvVar
from multienv.project import Project
from multienv.service import Service


class ProjectTestCase(unittest.TestCase):
    def test_get_services_names(self):
        config = Config(
            dot_env='fixtures/.env',
            env_var_container_build='fixtures/env_var_container_build.yml',
            projects='fixtures/Projects.yml'
        )
        project = Project(
            'site',
            [EnvVar('KEY', 'VALUE', config)],
            [Service('nginx'), Service('mysql')]
        )
        self.assertEqual(project.get_services_names(), ['nginx', 'mysql'])


if __name__ == '__main__':
    unittest.main()
