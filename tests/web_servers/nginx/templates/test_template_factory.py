import unittest

from multienv.web_servers.nginx.templates.default_template import \
    DefaultTemplate
from multienv.web_servers.nginx.templates.laravel_template import \
    LaravelTemplate
from multienv.web_servers.nginx.templates.symfony_template import \
    SymfonyTemplate
from multienv.web_servers.nginx.templates.template_factory import \
    TemplateFactory


class TemplateFactoryTestCase(unittest.TestCase):

    def test_create_for_template_laravel(self):
        factory = TemplateFactory('laravel')

        instance = factory.create('smartins.com', 'Projects/smartins.com')

        self.assertIsInstance(instance, LaravelTemplate)

    def test_create_for_symfony_template(self):
        factory = TemplateFactory('symfony')

        instance = factory.create('smartins.com', 'Projects/smartins.com')

        self.assertIsInstance(instance, SymfonyTemplate)

    def test_create_for_default_template(self):
        factory = TemplateFactory('default')

        instance = factory.create('smartins.com', 'Projects/smartins.com')

        self.assertIsInstance(instance, DefaultTemplate)

    def test_try_create_for_not_existent_template(self):
        with self.assertRaises(AttributeError):
            TemplateFactory('not_found').create('smartins.com',
                                                'Projects/smartins.com')


if __name__ == '__main__':
    unittest.main()
