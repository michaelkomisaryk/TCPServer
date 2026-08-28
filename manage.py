#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from symtable import Class


def main():


    class User:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    user = User("Alex", 16)
    user1 = User("jon", 20)
    user2 = User("anna", 25)
    print(f'{user.name}\n{user1.name}\n{user2.name}')


    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
