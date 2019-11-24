import abc

from multienv.exceptions import InvalidArgumentException
from multienv.web_servers.web_server_definitions import WebServerDefinitions


class WebServer:
    available_web_servers = [
        'nginx',
        'apache2',
        'caddy',
    ]
    laradock_root_folder = '..'

    def __init__(self, definitions, laradock_root_folder='..'):
        if not isinstance(definitions, WebServerDefinitions):
            raise InvalidArgumentException(
                error='The "definitions" param must be an instance of '
                      'WebServerDefinitions '
            )

        self.definitions = definitions
        self.laradock_root_folder = laradock_root_folder

    @abc.abstractmethod
    def create_domain(self):
        """
        Create a domain on service laradock folder

        Create config files to point to different project directory when
        visiting different domains.

        :param template: The template that will be used to create config file
        :type template: str
        """
        pass
