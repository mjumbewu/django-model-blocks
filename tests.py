"""
python setup.py test

"""
import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = 'example_project.settings'
from example_project import settings

settings.INSTALLED_APPS = (
    'example_project.pepulator_factory',
    'model_blocks',
)

def main():
    from django.test.utils import get_runner
    test_runner = get_runner(settings)(interactive=False)
    failures = test_runner.run_tests(['model_blocks',])
    sys.exit(failures)

if __name__ == '__main__':
    main()
