import unittest

from multienv.project.project import Project
from multienv.service import Service


class ProjectTestCase(unittest.TestCase):
    def test_get_services_names(self):
        project = Project(
            'site',
            [Service('nginx'), Service('mysql')])
        self.assertEqual(project.get_services_names(), ['nginx', 'mysql'])


if __name__ == '__main__':
    unittest.main()
