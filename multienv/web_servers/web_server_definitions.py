class WebServerDefinitions:
    name = None
    root = None
    template = None
    https = False
    default_template = 'laravel'

    def __init__(self, name, root, template=None, https=False):
        self.name = name
        self.root = root
        self.https = https

        if not template:
            template = self.default_template
        self.template = template
