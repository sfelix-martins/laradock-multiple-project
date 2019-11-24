import shutil

from multienv.web_servers.apache2.domain.templates.template import Template
from multienv.web_servers.web_server import WebServer


class Apache2(WebServer):
    def create_domain(self):
        site = self.definitions.name
        template_instance = Template(site, root=self.definitions.root)

        # Create a config file to site from template
        config_file_suffix = '.conf'
        sites_folder = self.laradock_root_folder + '/apache2/sites/'
        source = sites_folder + 'sample' + config_file_suffix + '.example'
        destination = sites_folder + site + config_file_suffix

        shutil.copyfile(source, destination)

        # Replace template configs
        template_instance.replace_content(destination)
