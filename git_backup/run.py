import argparse
import configparser
import multiprocessing as mp
import os
from abc import abstractmethod, ABCMeta
from subprocess import call
from github import Github
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import Repository


class GitIntegration(metaclass=ABCMeta):
    @abstractmethod
    def get_list_of_repos(self, backup_path, repositories_list):
        pass


class GithubIntegration(GitIntegration):
    def __init__(self, user, password):
        self._api = Github(user, password)

    def get_list_of_repos(self, backup_path, repositories_list):
        for repository in self._api.get_user().get_repos():
            info = {'name': os.path.join('github', repository.full_name),
                    'url': repository.ssh_url}
            info['local_path'] = os.path.join(backup_path, info['name'])

            repositories_list.append(info)


class BitbucketIntegration(GitIntegration):
    def __init__(self, user, email, password):
        self._api = Client(BasicAuthenticator(user, password, email))

    def get_list_of_repos(self, backup_path, repositories_list):
        for repository in Repository.find_repositories_by_owner_and_role(client=self._api):
            info = {'name': os.path.join('bitbucket', repository.full_name),
                    'url': repository.links['clone'][1]['href']}
            info['local_path'] = os.path.join(backup_path, info['name'])

            repositories_list.append(info)


class GitBackupRunner:
    def __init__(self, config):
        github_email = config.get('git-backup', 'GITHUB_EMAIL')
        github_pass = config.get('git-backup', 'GITHUB_PASS')
        bitbucket_user = config.get('git-backup', 'BITBUCKET_USER')
        bitbucket_email = config.get('git-backup', 'BITBUCKET_EMAIL')
        bitbucket_pass = config.get('git-backup', 'BITBUCKET_PASS')
        self._backup_path = config.get('git-backup', 'BACKUP_PATH')
        self._integrations = []

        if github_email and github_pass:
            github = GithubIntegration(github_email,
                                       github_pass)
            self._integrations.append(github)

        if bitbucket_user and bitbucket_email and bitbucket_pass:
            bitbucket = BitbucketIntegration(bitbucket_user,
                                             bitbucket_email,
                                             bitbucket_pass)
            self._integrations.append(bitbucket)

    def run(self):
        repositories_list = mp.Manager().list()

        processes = []
        for integration in self._integrations:
            processes.append(mp.Process(target=integration.get_list_of_repos,
                                        args=(self._backup_path, repositories_list)))
        [p.start() for p in processes]
        [p.join() for p in processes]

        repositories_queue = mp.Manager().Queue()
        [repositories_queue.put(r) for r in repositories_list]

        processes = []
        for i in range(0, 4):
            processes.append(mp.Process(target=GitBackupRunner.update_repository,
                                        args=(repositories_queue,)))
        [p.start() for p in processes]
        [p.join() for p in processes]

    @staticmethod
    def update_repository(repositories):
        while repositories.qsize():
            repository = repositories.get_nowait()

            if os.path.isdir(repository['local_path']) is False:
                os.makedirs(repository['local_path'])

            call(['git', 'init'], cwd=repository['local_path'])
            call(['git', 'remote', 'add', 'origin', repository['url']], cwd=repository['local_path'])
            call(['git', 'remote', 'prune', 'origin'], cwd=repository['local_path'])
            call(['git', 'remote', 'update'], cwd=repository['local_path'])


def main():
    parser = argparse.ArgumentParser(description='Git backup.')
    parser.add_argument('--config',
                        help='Path to config file.',
                        required=True)
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read_file(open(args.config))

    runner = GitBackupRunner(config)
    runner.run()


if __name__ == '__main__':
    main()
