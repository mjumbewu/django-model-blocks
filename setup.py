from setuptools import setup, find_packages

model_filters = __import__('model_filters')

readme_file = 'README.rst'
try:
    long_description = open(readme_file).read()
except IOError, err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

setup(name='django-model-filters',
      version='0.8.0',
      description='Simple filters for generic object template blocks',
      long_description=long_description,
      zip_safe=False,
      author='Mjumbe Wawatu Ukweli',
      author_email='mjumbewu@kwawatu.com',
      url='https://github.com/mjumbewu/django-model-filters/',
      download_url='https://github.com/mjumbewu/django-model-filters/downloads',
      packages = find_packages(exclude=['example_project', 'example_project.*']),
      include_package_data=True,
      install_requires = [
        'Django>=1.2.1',
      ],
      classifiers = ['Development Status :: 4 - Beta',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Utilities'],
      )

