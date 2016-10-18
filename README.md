# django-rotate-secret-key

This package adds a simple Django management command, to generate/regenerate a random 50-character secret key stored in a file specified by the `SECRET_KEY_FILE` setting.

## Installation

Install this package first, using the normal pip install:

```bash
pip install django-rotate-secret-key
```

Like any other Django app, add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
	...
	'django_rotate_secret_key',
	...
]
```

Then replace the `SECRET_KEY = '...'` line in your settings file with this:

```python
# Import key from an external file, so it doesn't get included in version control
SECRET_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secretkey.txt')
try:
	with open(SECRET_KEY_FILE, 'r') as f:
		SECRET_KEY = f.read().strip()
except:
	SECRET_KEY = '*** NOT CONFIGURED ***'
	print("WARNING: the SECRET_KEY setting has not yet been configured!")
```

This code will load the secret key from a separate file, so you can then exclude it from source control. The try/except block prevents Django from ever crashing due to an uninitialized SECRET_KEY variable (if it crashed at that stage, you wouldn't be able to create the first random key).

## Use

```bash
python manage.py rotate_secret_key [--force]
```

This will generate a new random secret key and save it to the `SECRET_KEY_FILE` file. If the file already exists, you'll see a "Replace this with a new key?" confirmation. The `--force` option removes that confirmation step.
