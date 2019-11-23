import unittest

from multienv.webservers.nginx.domain.templates.laraveltemplate import \
    LaravelTemplate
from multienv.webservers.nginx.domain.templates.templatefactory import \
    TemplateFactory


class TemplateFactoryTestCase(unittest.TestCase):

    def test_create_for_template_laravel(self):
        factory = TemplateFactory('laravel')

        instance = factory.create()

        self.assertIsInstance(instance, LaravelTemplate)

    def test_try_create_for_not_existent_template(self):
        with self.assertRaises(AttributeError):
            TemplateFactory('not_found').create()


if __name__ == '__main__':
    unittest.main()
