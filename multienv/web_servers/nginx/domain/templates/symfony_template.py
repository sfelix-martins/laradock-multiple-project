from multienv.helpers import sed_inplace
from multienv.web_servers.nginx.domain.templates.template import Template


class SymfonyTemplate(Template):
    def replace_content(self, filename):
        sed_inplace(filename, 'symfony.test', self.site)
        sed_inplace(filename,
                    'root /var/www/projects/symfony/web',
                    'root /var/www/' + self.root)
