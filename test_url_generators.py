import unittest
from url_generators import get_bitbucket_url, get_github_url


class BitBucketGenerationTestCase(unittest.TestCase):
    def test_full_defualt(self):
        generated = get_bitbucket_url("user")
        expected = "https://bitbucket.org/user/config/get/master.tar.gz"

        self.assertEqual(generated, expected)

    def test_repo(self):
        generated = get_bitbucket_url("user", repo='repo')
        expected = "https://bitbucket.org/user/repo/get/master.tar.gz"

        self.assertEqual(generated, expected)

    def test_commit(self):
        generated = get_bitbucket_url("user", commit='develop')
        expected = "https://bitbucket.org/user/config/get/develop.tar.gz"

        self.assertEqual(generated, expected)


class GitHubGenerationTestCase(unittest.TestCase):
    def test_full_default(self):
        generated = get_github_url("user")
        expected = "https://github.com/user/config/tarball/master"

        self.assertEqual(generated, expected)

    def test_repo(self):
        generated = get_github_url("user", repo='repo')
        expected = "https://github.com/user/repo/tarball/master"

        self.assertEqual(generated, expected)

    def test_commit(self):
        generated = get_github_url("user", commit='develop')
        expected = "https://github.com/user/config/tarball/develop"

        self.assertEqual(generated, expected)


if __name__ == '__main__':
    unittest.main()
