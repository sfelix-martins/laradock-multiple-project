from multienv.webservers.nginx.domain.templates.laraveltemplate import \
    LaravelTemplate


class TemplateFactory:
    template = None

    def __init__(self, template):
        self.template = template

    def create(self):
        if self.template == 'laravel':
            return LaravelTemplate()

        raise AttributeError
