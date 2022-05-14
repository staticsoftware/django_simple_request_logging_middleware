

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_simple_request_logging_middleware',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Barebones request logging for django apps',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://staticdata.io/',
    author='Static Software',
    author_email='support@staticdata.io',
    install_requires=[
        "django-json-widget",
    ],
    python_requires='>=3.9',
    keywords="django http request logging event tracking",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    project_urls={
        'Documentation': 'https://github.com/radding/django-events/blob/master/README.md',
        'Source': 'https://github.com/radding/django-events/',
        'Tracker': 'https://github.com/radding/django-events/issues',
    },
)