
## How to run ##
- - - -

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

_Migrations included_

_user: admin password: admin123p has access to admin/_ 

## How to test ##

-get latest geckodriver from https://github.com/mozilla/geckodriver/releases

-add it to PATH

### events app unittests ###
```bash
python manage.py test --keepdb apps.events
```

### accounts app unittests ###
```bash
python manage.py test --keepdb apps.accounts
```

### functional tests ###
```bash
python manage.py test --keepdb functional_tests
```

### all tests at once ###
```bash
python manage.py test --keepdb
```
