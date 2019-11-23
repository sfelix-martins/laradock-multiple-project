import unittest

from multienv.exceptions import InvalidArgumentException
from multienv.webservers.nginx.nginx import Nginx
from multienv.webservers.web_server_factory import WebServerFactory
from multienv.webservers.webserver import WebServer


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
            .create(definitions, laradock_root_folder='tests/fixtures/laradock')
        self.assertIsInstance(web_server, WebServer)
        self.assertIsInstance(web_server, Nginx)


if __name__ == '__main__':
    unittest.main()
