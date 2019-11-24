from multienv.helpers import sed_inplace
from multienv.web_servers.nginx.templates.template import Template


class LaravelTemplate(Template):
    def replace_content(self, filename):
        sed_inplace(filename, 'laravel.test', self.site)
        sed_inplace(filename,
                    'root /var/www/laravel/public',
                    'root /var/www/' + self.root)
