import unittest
import shutil
import os

from multienv.web_servers.caddy.caddy_template import CaddyTemplate


class CaddyTemplateTestCase(unittest.TestCase):
    fixtures_folder = 'tests/fixtures/'

    def test_replace_content(self):
        filename = self.fixtures_folder + \
                   'laradock/caddy/caddy/Caddyfile'
        shutil.copyfile('multienv/web_servers/caddy/Caddyfile', filename)

        site = 'test.com'
        root = 'Project/test.com/public'

        test_filename = shutil.copyfile(filename, filename + '.test')

        print('Test filenma', test_filename)

        template = CaddyTemplate(site, root)
        template.replace_content(test_filename)

        server_name = ''
        document_roots = []
        https = True
        with open(test_filename) as src_file:
            for line in src_file:
                if ':80 {' in line and 'demo' not in line:
                    server_name = line.partition(':80 {')[0]
                if 'root /var/www/' in line:
                    document_roots.append(line)
                if '#tls self_signed' in line:
                    https = False

        self.assertEqual(site, server_name.strip())
        for document_root in document_roots:
            self.assertEqual('root /var/www/' + root, document_root.strip())
        self.assertFalse(https)

        os.remove(test_filename)

    def test_replace_content_with_https(self):
        filename = self.fixtures_folder + \
                   'laradock/caddy/caddy/Caddyfile'
        shutil.copyfile('multienv/web_servers/caddy/Caddyfile', filename)

        site = 'test.com'
        root = 'Project/test.com/public'

        test_filename = shutil.copyfile(filename, filename + '.test')

        template = CaddyTemplate(site, root, https=True)
        template.replace_content(test_filename)

        server_name = ''
        document_roots = []
        https = False
        with open(test_filename) as src_file:
            for line in src_file:
                if ':80 {' in line and 'demo' not in line:
                    server_name = line.partition(':80 {')[0]
                if 'root /var/www/' in line:
                    document_roots.append(line)
                if 'tls self_signed' in line and '#' not in line:
                    https = True

        self.assertEqual('https://' + site, server_name.strip())
        for document_root in document_roots:
            self.assertEqual('root /var/www/' + root, document_root.strip())
        self.assertTrue(https)

        os.remove(test_filename)


if __name__ == '__main__':
    unittest.main()
