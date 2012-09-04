import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name = 'alto',
    version = '0.3.1',
    description = 'A high-level code browser for Django projects.',
    long_description = README,
    author = 'Joseph Kocherhans',
    author_email = 'joseph@jkocherhans.com',
    license='BSD',
    url='http://github.com/jkocherhans/alto',
    packages = ['alto'],
    include_package_data = True,
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'Django>=1.4'
    ]
)
