import unittest
import shutil
import os

from multienv.web_servers.apache2.domain.templates.template import Template


class TemplateTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures/'

    def test_replace_content(self):
        filename = self.fixtures_folder + \
                   'laradock/apache2/sites/sample.conf.example'
        site = 'test.com'
        root = 'Project/test.com/public'

        test_filename = shutil.copyfile(filename, filename + '.test')

        template = Template(site, root)
        template.replace_content(test_filename)

        server_name = ''
        document_root = ''
        directory = ''
        with open(test_filename) as src_file:
            for line in src_file:
                if 'ServerName' in line:
                    server_name = line.partition('ServerName')[2]
                if 'DocumentRoot /var/www/' in line:
                    document_root = line.partition('DocumentRoot')[2]
                if '<Directory "/var/www' in line:
                    directory = line

        self.assertEqual(site, server_name.strip())
        self.assertEqual('/var/www/' + root, document_root.strip())
        self.assertEqual('<Directory "/var/www/Project/test.com/public">',
                         directory.strip())

        os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()
