from multienv.web_servers.nginx.templates.default_template import \
    DefaultTemplate
from multienv.web_servers.nginx.templates.laravel_template import \
    LaravelTemplate
from multienv.web_servers.nginx.templates.symfony_template import \
    SymfonyTemplate


class TemplateFactory:
    template = None

    def __init__(self, template):
        self.template = template

    def create(self, name, root):
        if self.template == 'laravel':
            return LaravelTemplate(name, root)

        if self.template == 'symfony':
            return SymfonyTemplate(name, root)

        if self.template == 'default':
            return DefaultTemplate(name, root)

        raise AttributeError
