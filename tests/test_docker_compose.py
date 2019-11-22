import unittest
import mock


from multienv.docker_compose import DockerCompose


class DockerComposeTestCase(unittest.TestCase):
    def test_build_cmd(self):
        dc = DockerCompose()
        dc.build('apache')

        self.assertEqual('docker-compose build apache', dc.cmd)

    def test_down_cmd(self):
        dc = DockerCompose()
        dc.down()

        self.assertEqual('docker-compose down', dc.cmd)

    def test_up_cmd_not_detached(self):
        dc = DockerCompose()
        dc.up(['apache', 'mysql', 'mailhog'], detached=False)

        self.assertEqual('docker-compose up apache mysql mailhog', dc.cmd)

    def test_up_cmd_detached(self):
        dc = DockerCompose()
        dc.up(['apache', 'mysql', 'mailhog'], detached=True)

        self.assertEqual('docker-compose up -d apache mysql mailhog', dc.cmd)

    def test_exec_cmd_with_user(self):
        dc = DockerCompose()
        dc.execute(['workspace', 'bash'], user='laradock')

        self.assertEqual('docker-compose exec --user=laradock workspace bash',
                         dc.cmd)

    def test_exec_cmd_without_user(self):
        dc = DockerCompose()
        dc.execute(['workspace', 'bash'])

        self.assertEqual('docker-compose exec workspace bash', dc.cmd)

    def test_call_cmd_without_mount(self):
        with self.assertRaises(RuntimeError):
            dc = DockerCompose()
            dc.call()

    @mock.patch('subprocess.call')
    def test_call_cmd(self, mock_subprocess):
        dc = DockerCompose()
        dc.up(['apache', 'mysql'], detached=True).call()

        self.assertTrue(mock_subprocess.called)


if __name__ == '__main__':
    unittest.main()
