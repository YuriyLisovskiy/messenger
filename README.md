# Messenger

This is a simple messenger. Currently it support creating user profile, editing it and massaging. Also there are music music app. But it is not tested, so there can be some bugs.
Also administrator account is not available now. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

First you need python3 interpreter

If you want to make some changes and add other modules, create a virtual environment:

```
virtualenv venv
```

Activate your virtual environment.

Linux (using `source`):

```
source venv/bin/activate
```

Windows:

```
source venv/Scripts/activate
```

Also there are some modules you need to install to prevent an issues:

```
dj-static==0.0.6
Django==1.11.4
djangorestframework==3.6.4
olefile==0.44
Pillow==4.2.1
pytz==2017.2
static3==0.7.0
```

Or you can install all requirement modules from `requirements.txt` file:
```
pip install -r requirements.txt
```

### Installing

A step by step series of examples that tell you have to get a development env running.

Clone the repository:
```
git clone https://github.com/YuriyLisovskiy/messenger.git
```
Run the server: 
```
cd messenger
python manage.py runserver
```
Or you can start the server with you own ip and port.

For example: 
```
python manage.py runserver 123.123.1.123:1234
```
Open in browser `https://127.0.0.1:8000` if you run the server with default parameters, otherwise open `https://123.123.1.123:1234` as in the example.

## Authors

**[Yuriy Lisovskiy](https://github.com/YuriyLisovskiy)** - *All work*


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
