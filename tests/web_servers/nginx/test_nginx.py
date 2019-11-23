import unittest
import os

from multienv.web_servers.nginx.nginx import Nginx
from multienv.web_servers.web_server_definitions import WebServerDefinitions


class NginxTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures'

    def test_create_domain_config_file(self):
        definitions = WebServerDefinitions(name='smartins.com',
                                           root='Projects/sites/smartins.com')

        nginx = Nginx(definitions,
                      laradock_root_folder=self.fixtures_folder + '/laradock')
        nginx.create_domain(template='laravel')

        site_config_file = self.fixtures_folder + '/laradock/nginx/sites' \
                                                  '/smartins.com.conf'

        # Assert the site config file exists
        self.assertTrue(os.path.isfile(site_config_file))

        # Clear tests side effects
        os.remove(site_config_file)


if __name__ == '__main__':
    unittest.main()
