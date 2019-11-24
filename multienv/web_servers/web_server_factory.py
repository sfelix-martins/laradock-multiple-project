from multienv.exceptions import InvalidArgumentException, \
    InvalidProjectDefinitions
from multienv.web_servers.apache2.apache2 import Apache2
from multienv.web_servers.caddy.caddy import Caddy
from multienv.web_servers.nginx.nginx import Nginx
from multienv.web_servers.web_server_definitions import WebServerDefinitions
from multienv.web_servers.web_server import WebServer


class WebServerFactory:
    name = None

    def __init__(self, name):
        if name not in WebServer.available_web_servers:
            raise InvalidArgumentException(
                error='WebServer [' + name + '] not found',
                hint='You must choose one of these: ['
                     + ', '.join(WebServer.available_web_servers) + ']'
            )

        self.name = name

    def create(self, server_definitions, laradock_root_folder):
        server_name = server_definitions.get('name')
        root_folder = server_definitions.get('root')
        if not server_name or not root_folder:
            raise InvalidProjectDefinitions(
                error='The "server" definition is wrong',
                hint='You must define the keys "name" and "root" with the '
                     'server mapping'
            )

        server_definitions = WebServerDefinitions(server_name, root_folder)

        if self.name == 'nginx':
            return Nginx(definitions=server_definitions,
                         laradock_root_folder=laradock_root_folder)

        if self.name == 'apache2':
            return Apache2(definitions=server_definitions,
                           laradock_root_folder=laradock_root_folder)

        if self.name == 'caddy':
            return Caddy(definitions=server_definitions,
                         laradock_root_folder=laradock_root_folder)

        return
