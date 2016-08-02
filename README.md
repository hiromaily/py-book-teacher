# py-book-teacher
Go-book-teacher is for booking specific teachers on English lesson service by web scraping.
After finding teachers are available, notification by E-mail or Open Browser is run.



Before running, duplicate config.default.ini as config.ini.

## requirement
* python version: ```3.5``` or later
(because of parallel processing)


## Installation

### For mac local
```
[pyenv]
$ pyenv versions
$ pyenv global 3.5.1
$ pyenv rehash
```

```
[venv]
$ mkdir book
$ pyvenv book
$ source book/bin/activate
```

```
[pip]
$ easy_install pip
$ pip install -r pip_packages.txt
```

```
[execution]
$ ./book.py
```
```
[clean]
$ deactivate

```

### For docker environment
This is easy setup.
```
$ ./docker-create.sh
```


## Configration

### 1. Common settings
#### copy ini file
```
$ cp config.default.ini config.ini
```

####  modify config.ini file
```
# parallel processing
parallel = 1
```

```
# when it found teachers and state was changed, open browser as notification.
browser = 1
```

```
[mail]
# when it found teachers and state was changed, send e-mail as notification.
enable = 1
```

#### registration for target teacher's ids
Target file is ```./data/teachers.json```. Modify it as your preference.


### 2. On Docker

#### Docker related files
* docker-create.sh
* docker-compose.yml
* docker-entrypoint.sh
* Dockerfile
* ./docker_build/*



