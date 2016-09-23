from setuptools import setup

config = {
    'name': 'git-backup',
    'version': '1.0.0',
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
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
