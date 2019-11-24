import unittest
import os

from multienv.web_servers.caddy.caddy import Caddy
from multienv.web_servers.web_server_definitions import WebServerDefinitions


class CaddyTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures'

    def test_create_domain_config_file(self):
        site = 'smartins.com'
        root = 'Projects/sites/smartins.com'
        definitions = WebServerDefinitions(name=site, root=root)

        caddy = Caddy(definitions,
                      laradock_root_folder=self.fixtures_folder + '/laradock')
        caddy.create_domain()

        site_config_file = self.fixtures_folder + '/laradock/caddy/Caddyfile'

        # Assert the site config file exists
        self.assertTrue(os.path.isfile(site_config_file))

        # Check config file content
        server_name = ''
        document_roots = []
        https = True
        with open(site_config_file) as src_file:
            for line in src_file:
                if ':80 {' in line and 'demo' not in line:
                    server_name = line.partition(':80 {')[0]
                if 'root /var/www/' in line:
                    document_roots.append(line)
                if '#tls self_signed' in line:
                    https = False

        self.assertEqual(site, server_name.strip())
        for document_root in document_roots:
            self.assertEqual('root /var/www/' + root, document_root.strip())
        self.assertFalse(https)

    def test_create_domain_config_file_with_https(self):
        site = 'smartins.com'
        root = 'Projects/sites/smartins.com'
        definitions = WebServerDefinitions(name=site, root=root, https=True)

        caddy = Caddy(definitions,
                      laradock_root_folder=self.fixtures_folder + '/laradock')
        caddy.create_domain()

        site_config_file = self.fixtures_folder + '/laradock/caddy/Caddyfile'

        # Assert the site config file exists
        self.assertTrue(os.path.isfile(site_config_file))

        # Check config file content
        server_name = ''
        document_roots = []
        https = False
        with open(site_config_file) as src_file:
            for line in src_file:
                if ':80 {' in line and 'demo' not in line:
                    server_name = line.partition(':80 {')[0]
                if 'root /var/www/' in line:
                    document_roots.append(line)
                if 'tls self_signed' in line and '#' not in line:
                    https = True

        self.assertEqual('https://' + site, server_name.strip())
        for document_root in document_roots:
            self.assertEqual('root /var/www/' + root, document_root.strip())
        self.assertTrue(https)


if __name__ == '__main__':
    unittest.main()
