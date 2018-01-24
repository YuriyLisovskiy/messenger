# Messenger
[![Build Status](https://travis-ci.org/YuriyLisovskiy/Messenger.svg)](https://github.com/YuriyLisovskiy/Messenger)
[![Coverage Status](https://coveralls.io/repos/github/YuriyLisovskiy/Messenger/badge.svg)](https://github.com/YuriyLisovskiy/Messenger)

This is a simple messenger. Currently it supports creating user profile, editing it and massaging. Also there are music app. But it is not tested, so there can be some bugs.
Also administrator account is not available now. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

You need Python3.6

### Installing and Running

A step by step series of examples that tell you have to get a development env running:

Linux:
```
git clone https://github.com/YuriyLisovskiy/messenger.git
cd messenger
virtualenv venv
venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
python manage.py runserver
```

Windows:
```
git clone https://github.com/YuriyLisovskiy/messenger.git
cd messenger
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
python manage.py runserver
```
Or you can start the server with you own ip address and port.

For example: 
```
python manage.py runserver 123.123.1.123:1234
```
Open in browser `https://127.0.0.1:8000` if you run the server with default parameters, otherwise open `https://123.123.1.123:1234` as in the example.

## Authors

**[Yuriy Lisovskiy](https://github.com/YuriyLisovskiy)** - *All work*


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
