# Git backup.

##

Backups all of your git repositories ([GitHub](https://github.com/) / [Bitbucket](https://bitbucket.org/)) locally.


### What do I need?
- Python 3.5


### How to run it?

#### Install by hand

```
$ git clone <address here>
```

#### Install from pypi
```
$ pip install git-backup
```

#### Configure it
1. Create configuration file, you can see example inside of `git_backup/config.cfg.dist`
2. Set your Github/Bitbucket access token and path to where repositories will be stored

#### Execute it
If you installed it by hand
```
$ python git_backup/run.py
```

If you installed it with pypi
```
$ git_backup_run
```

### Faq
Q: How can I export it to Google Drive/Dropbox/etc.

A: Just set `BACKUP_PATH` from `config.py` to a path that is synchronised with your cloud storage
