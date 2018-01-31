# Messenger
| **`License`** | **`Language`** | **`AppVeyor`** | **`Travis CI`** | **`Coveralls`** |
|-----------------|---------------------|------------------|-------------------|---------------|
|[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE) | [![Language](https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg)](https://github.com/YuriyLisovskiy/Messenger) | [![Build status](https://ci.appveyor.com/api/projects/status/kx19qjie8ysvs15l?svg=true)](https://ci.appveyor.com/project/YuriyLisovskiy/messenger) | [![Build Status](https://travis-ci.org/YuriyLisovskiy/Messenger.svg)](https://github.com/YuriyLisovskiy/Messenger) | [![Coverage Status](https://coveralls.io/repos/github/YuriyLisovskiy/Messenger/badge.svg)](https://github.com/YuriyLisovskiy/Messenger) |
## Installation
Linux:
```bash
$ git clone https://github.com/YuriyLisovskiy/Messenger.git
$ cd Messenger/
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
```
Windows:
```bash
$ git clone https://github.com/YuriyLisovskiy/Messenger.git
$ cd Messenger/
$ virtualenv venv
$ venv/Scripts/activate
$ pip install -r requirements.txt
$ python manage.py migrate
```
Start the server: 
```
$ python manage.py runserver
```
## Author
- **[Yuriy Lisovskiy](https://github.com/YuriyLisovskiy)**
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
