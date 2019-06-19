import os
import sys

import click
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from github import Github
from tqdm import tqdm


@click.command()
@click.option("--path", required=True, help="Path to where repositories will be saved.")
def cli(path):
    repos = github_integration(path)

    for repo in tqdm(repos, bar_format="Processing github repositories: {n}"):
        local_repository_path = os.path.join(path, "github", repo["name"])

        try:
            repo = Repo(local_repository_path)
        except (InvalidGitRepositoryError, NoSuchPathError):
            if not os.path.isdir(local_repository_path):
                os.makedirs(local_repository_path)
            repo = Repo.clone_from(
                f"https://github.com/{repo['name']}.git", local_repository_path
            )

        for remote in repo.remotes:
            remote.fetch()
            remote.pull()

        repo.submodule_update()


def github_integration(path):
    _validate({"GITHUB_TOKEN"})

    github = Github(os.environ["GITHUB_TOKEN"])
    github_repos = github.get_user().get_repos()

    for r in github_repos:
        yield {"name": r.full_name}


def _validate(required_envs):
    missing_env = required_envs - os.environ.keys()
    if missing_env:
        click.secho(f'Missing env variables: "{",".join(missing_env)}".', fg="red")
        sys.exit()


if __name__ == "__main__":
    cli()
