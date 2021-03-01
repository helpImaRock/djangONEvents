
## How to run ##
- - - -

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip3 -r install requirements.txt
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
