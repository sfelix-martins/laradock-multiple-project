import shutil

from multienv.webservers.nginx.domain.templates.templatefactory import \
    TemplateFactory
from multienv.webservers.webserver import WebServer


class Nginx(WebServer):
    def create_domain(self, template='laravel'):
        template_instance = TemplateFactory(template).create()

        site = self.definitions.name

        # Create a config file to site from template
        config_file_suffix = '.conf'
        sites_folder = self.laradock_root_folder + '/nginx/sites/'
        source = sites_folder + template + config_file_suffix + '.example'
        destination = sites_folder + site + config_file_suffix

        shutil.copyfile(source, destination)

        # Replace template configs
        template_instance.replace_content(destination,
                                          site,
                                          self.definitions.root)
