from multienv.helpers import sed_inplace
from multienv.web_servers.nginx.domain.templates.template import Template


class DefaultTemplate(Template):
    def replace_content(self, filename):
        sed_inplace(filename, 'app.test', self.site)
        sed_inplace(filename,
                    'root /var/www/app',
                    'root /var/www/' + self.root)
