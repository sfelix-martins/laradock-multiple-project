import unittest
import shutil
import os

from multienv.web_servers.nginx.domain.templates.default_template import \
    DefaultTemplate


class DefaultTemplateTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures/'

    def test_replace_content(self):
        filename = self.fixtures_folder + \
                   'laradock/nginx/sites/app.conf.example'
        site = 'test.com'
        root = 'Project/test.com'

        test_filename = shutil.copyfile(filename, filename + '.test')

        template = DefaultTemplate(site, root)
        template.replace_content(test_filename)

        server_name = ''
        root_folder = ''
        with open(test_filename) as src_file:
            for line in src_file:
                if 'server_name' in line:
                    server_name = line.partition('server_name')[2]
                if 'root /var/www/' in line and \
                        '/var/www/letsencrypt/;' not in line:
                    root_folder = line.partition('root')[2]

        self.assertEqual(site + ';', server_name.strip())
        self.assertEqual('/var/www/' + root + ';', root_folder.strip())

        os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()
