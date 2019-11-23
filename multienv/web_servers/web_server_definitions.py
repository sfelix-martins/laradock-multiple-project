class WebServerDefinitions:
    name = None
    root = None
    template = None
    default_template = 'laravel'

    def __init__(self, name, root, template=None):
        self.name = name
        self.root = root

        if not template:
            template = self.default_template
        self.template = template
