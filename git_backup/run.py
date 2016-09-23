import argparse
import configparser
import os

from abc import ABCMeta, abstractmethod
from subprocess import call
from github import Github
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import Repository


class GitIntegration(metaclass=ABCMeta):
    @abstractmethod
    def get_list_of_repos(self):
        pass

    def refresh_list_of_projects(self, path):
        for info in self.get_list_of_repos():
            repo_path = path + '/' + info['name']

            if os.path.isdir(repo_path) is False:
                os.makedirs(repo_path)

                call(['git', 'init'], cwd=repo_path)
                call(['git', 'remote', 'add', 'origin', info['url']], cwd=repo_path)

    def refresh_projects(self, path):
        for directory in [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]:
            working_dir = path + '/' + directory

            call(['git', 'remote', 'prune', 'origin'], cwd=working_dir)
            call(['git', 'remote', 'update'], cwd=working_dir)


class GithubIntegration(GitIntegration):
    def __init__(self, user, password):
        self._api = Github(user, password)

    def get_list_of_repos(self):
        result = []

        for repo in self._api.get_user().get_repos():
            info = {'name': repo.name,
                    'url': repo.ssh_url}
            result.append(info)

        return result


class BitbucketIntegration(GitIntegration):
    def __init__(self, user, email, password):
        self._api = Client(
            BasicAuthenticator(user, password, email)
        )

    def get_list_of_repos(self):
        result = []

        for repository in Repository.find_repositories_by_owner_and_role(client=self._api):
            info = {'name': repository.name,
                    'url': repository.links['clone'][1]['href']}
            result.append(info)

        return result


class GitBackupRunner:
    def execute(self, args):
        integrations = []

        config = configparser.ConfigParser()
        config.read_file(open(args.config))

        github_email = config.get('git-backup', 'GITHUB_EMAIL')
        github_pass = config.get('git-backup', 'GITHUB_PASS')
        bitbucket_user = config.get('git-backup', 'BITBUCKET_USER')
        bitbucket_email = config.get('git-backup', 'BITBUCKET_EMAIL')
        bitbucket_pass = config.get('git-backup', 'BITBUCKET_PASS')
        backup_path = config.get('git-backup', 'BACKUP_PATH')

        if github_email and github_pass:
            github = GithubIntegration(github_email,
                                       github_pass)
            integrations.append(github)

        if bitbucket_user and bitbucket_email and bitbucket_pass:
            bitbucket = BitbucketIntegration(bitbucket_user,
                                             bitbucket_email,
                                             bitbucket_pass)
            integrations.append(bitbucket)

        if args.refresh_list_of_projects:
            for integration in integrations:
                integration.refresh_list_of_projects(backup_path)

        if args.refresh_projects:
            for integration in integrations:
                integration.refresh_projects(backup_path)

    def run(self):
        parser = argparse.ArgumentParser(description='Git backup.')
        parser.add_argument('--refresh-list-of-projects',
                            help='Loads list of projects from remote servers.',
                            nargs='?',
                            default=False,
                            const=True)
        parser.add_argument('--refresh-projects',
                            help='Loads content of projects from remote servers.',
                            nargs='?',
                            default=False,
                            const=True)
        parser.add_argument('--config',
                            help='Path to config file.',
                            required=True)

        args = parser.parse_args()

        self.execute(args)


def main():
    runner = GitBackupRunner()
    runner.run()

if __name__ == '__main__':
    main()
