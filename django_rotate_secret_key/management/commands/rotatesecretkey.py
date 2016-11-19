import os
import string
import random
from django.core.management.base import BaseCommand
from django.utils import six
from django.utils.six.moves import input
from django.conf import settings

class Command(BaseCommand):
	help = "Generate/regenerate a random 50-character secret key stored in a file specified by the `SECRET_KEY_FILE` setting."

	def add_arguments(self, parser):
		parser.add_argument(
			'--force',
			action='store_true',
			dest='force',
			default=False,
			help='Replace the existing key without prompting'
		)

	def handle(self, *args, **options):
		# Find the key file (this setting must exist)
		try:
			key_file = settings.SECRET_KEY_FILE
		except:
			self.stderr.write('SECRET_KEY_FILE not configured!')
			exit(2)

		# If the file exists and already has contents, then only replace if --force argument was given
		existing_key = ''
		try:
			existing_key = open(key_file).read().strip()
		except:
			pass # No key file found, so we're safe to create a new one without prompting
		else:
			if existing_key:
				self.stdout.write("EXISTING SECRET KEY: {}".format(existing_key))
				if not options.get('force'):
					if input("Replace this with a new key? [y/N] ").lower() != 'y': return

		self.stdout.write('')

		# Generate new key
		char_list = string.ascii_letters + string.digits + string.punctuation
		generated_key = ''.join([random.SystemRandom().choice(char_list) for _ in range(50)])
		self.stdout.write("NEW SECRET KEY:      {}".format(generated_key))

		# Create directory if it doesn't already exist
		key_dir = os.path.dirname(key_file)
		if six.PY2:
			if not os.path.isdir(key_dir):
				os.makedirs(key_dir)
		else:
			os.makedirs(key_dir, exist_ok=True)

		# Write new key to file
		with open(key_file, 'w') as f:
			f.write(generated_key)
		self.stdout.write("Written to {}".format(key_file))
