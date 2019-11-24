import unittest
import shutil
import os

from multienv.web_servers.nginx.templates.symfony_template import \
    SymfonyTemplate


class SymfonyTemplateTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures/'

    def test_replace_content(self):
        filename = self.fixtures_folder + \
                   'laradock/nginx/sites/symfony.conf.example'
        site = 'test.com'
        root = 'Project/test.com/web'

        test_filename = shutil.copyfile(filename, filename + '.test')

        SymfonyTemplate(site, root).replace_content(test_filename)

        server_name = ''
        root_folder = ''
        with open(test_filename) as src_file:
            for line in src_file:
                if 'server_name' in line:
                    server_name = line.partition('server_name')[2]
                if 'root /var/www/' in line:
                    root_folder = line.partition('root')[2]

        self.assertEqual(site + ';', server_name.strip())
        self.assertEqual('/var/www/' + root + ';', root_folder.strip())

        os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()
