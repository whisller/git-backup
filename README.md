# Git backup.

##

Backups all of your remote git repositories ([GitHub](https://github.com/) / [Bitbucket](https://bitbucket.org/)) locally.


### What do I need?
- Python 3.5


### How to run it?

#### Install by hand

```
$ git clone https://github.com/whisller/git-backup.git
```

#### Configure it
1. Create configuration file, you can see example inside of `git_backup/config.cfg.dist`
2. Set your Github/Bitbucket access token and path to where repositories will be stored

#### Install dependencies
```
$ python setup.py install
```

#### Execute it
```
$ python git_backup/run.py
```
or
```
$ git_backup_run
```

### FAQ
Q: How can I export it to Google Drive/Dropbox/etc.

A: Just set `BACKUP_PATH` from `config.py` to a path that is synchronised with your cloud storage
