from setuptools import setup

config = {
    'name': 'git-repo-backup',
    'version': '1.2.0',
    'description': 'Backups all of your remote git repositories (Github/Bitbucket) locally.',
    'keywords': ['git', 'github', 'bitbucket', 'backup'],
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
    'url': 'https://github.com/whisller/git-backup',
    'packages': [
        'git_backup'
    ],
    'scripts': ['bin/git_backup_run'],
    'install_requires': [
        'PyGithub==1.28',
        'pybitbucket==0.11.1'
    ]
}

setup(**config)
