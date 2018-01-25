# Messenger
[![Build Status](https://travis-ci.org/YuriyLisovskiy/Messenger.svg)](https://github.com/YuriyLisovskiy/Messenger)
[![Coverage Status](https://coveralls.io/repos/github/YuriyLisovskiy/Messenger/badge.svg)](https://github.com/YuriyLisovskiy/Messenger)
[![Licence Status](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

### Download and Configure

Linux:
```
git clone https://github.com/YuriyLisovskiy/Messenger.git
cd Messenger/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

Windows:
```
git clone https://github.com/YuriyLisovskiy/messenger.git
cd Messenger/
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
```

Start the server: 
```
python manage.py runserver
```

### Author

* **[Yuriy Lisovskiy](https://github.com/YuriyLisovskiy)**


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
