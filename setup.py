from setuptools import setup, find_packages

model_blocks = __import__('model_blocks')

readme_file = 'README.rst'
try:
    long_description = open(readme_file).read()
except IOError, err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

setup(name='django-model-blocks',
      version='0.8.1',
      description=('Simple filters and tags for generic Django '
                   'model template partials'),
      long_description=long_description,
      zip_safe=False,
      author='Mjumbe Wawatu Ukweli',
      author_email='mjumbewu@kwawatu.com',
      url='https://github.com/mjumbewu/django-model-blocks/',
      download_url='https://github.com/mjumbewu/django-model-blocks/downloads',
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

