import shutil

from multienv.web_servers.nginx.templates.template_factory import \
    TemplateFactory
from multienv.web_servers.web_server import WebServer


class Nginx(WebServer):
    def create_domain(self):
        template = self.definitions.template

        template_instance = TemplateFactory(template).create(
            name=self.definitions.name,
            root=self.definitions.root
        )

        site = self.definitions.name

        # Create a config file to site from template
        config_file_suffix = '.conf'
        sites_folder = self.laradock_root_folder + '/nginx/sites/'
        source = sites_folder + template + config_file_suffix + '.example'
        destination = sites_folder + site + config_file_suffix

        shutil.copyfile(source, destination)

        # Replace template configs
        template_instance.replace_content(destination)
