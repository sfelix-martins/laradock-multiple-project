import shutil
import os

from multienv.web_servers.caddy.caddy_template import CaddyTemplate
from multienv.web_servers.web_server import WebServer


class Caddy(WebServer):
    def create_domain(self):
        site = self.definitions.name
        template_instance = CaddyTemplate(site,
                                          root=self.definitions.root,
                                          https=self.definitions.https)

        source = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              'Caddyfile'))

        destination = self.laradock_root_folder + '/caddy/caddy/Caddyfile'

        shutil.copyfile(source, destination)

        # Replace template configs
        template_instance.replace_content(destination)