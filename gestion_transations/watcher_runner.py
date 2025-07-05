import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_transations.settings")
django.setup()

from application.watcher import start_file_watcher

if __name__ == '__main__':
    start_file_watcher()
