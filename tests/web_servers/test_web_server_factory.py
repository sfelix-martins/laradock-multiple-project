import unittest

from multienv.exceptions import InvalidArgumentException
from multienv.web_servers.apache2.apache2 import Apache2
from multienv.web_servers.caddy.caddy import Caddy
from multienv.web_servers.nginx.nginx import Nginx
from multienv.web_servers.web_server_factory import WebServerFactory
from multienv.web_servers.web_server import WebServer


class WebServerFactoryTestCase(unittest.TestCase):
    def test_create_with_not_existent_server_service(self):
        with self.assertRaises(InvalidArgumentException):
            WebServerFactory('mysql')

    def test_create_nginx_server_service(self):
        definitions = {
            'name': 'samuelmartins.dev',
            'root': 'Projects/sites/samuelmartins.dev'
        }

        web_server = WebServerFactory('nginx')\
            .create(definitions,
                    laradock_root_folder='tests/fixtures/laradock')
        self.assertIsInstance(web_server, WebServer)
        self.assertIsInstance(web_server, Nginx)

    def test_create_apache2_server_service(self):
        definitions = {
            'name': 'samuelmartins.dev',
            'root': 'Projects/sites/samuelmartins.dev'
        }

        web_server = WebServerFactory('apache2') \
            .create(definitions,
                    laradock_root_folder='tests/fixtures/laradock')
        self.assertIsInstance(web_server, WebServer)
        self.assertIsInstance(web_server, Apache2)

    def test_create_caddy_server_service_with_https(self):
        definitions = {
            'name': 'samuelmartins.dev',
            'root': 'Projects/sites/samuelmartins.dev',
            'https': True,
        }

        web_server = WebServerFactory('caddy') \
            .create(definitions,
                    laradock_root_folder='tests/fixtures/laradock')
        self.assertIsInstance(web_server, WebServer)
        self.assertIsInstance(web_server, Caddy)

    def test_create_caddy_server_service_without_https(self):
        definitions = {
            'name': 'samuelmartins.dev',
            'root': 'Projects/sites/samuelmartins.dev',
            'https': False,
        }

        web_server = WebServerFactory('caddy') \
            .create(definitions,
                    laradock_root_folder='tests/fixtures/laradock')
        self.assertIsInstance(web_server, WebServer)
        self.assertIsInstance(web_server, Caddy)


if __name__ == '__main__':
    unittest.main()
