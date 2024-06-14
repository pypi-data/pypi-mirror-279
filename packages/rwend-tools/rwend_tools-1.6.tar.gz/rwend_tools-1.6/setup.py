#%%

from setuptools import setup, find_packages

setup(
    name='rwend_tools',
    version='1.6',
    packages=['rwend_tools'],
    install_requires=[
        'pyyaml',
        'googlemaps',
        'google-cloud-secret-manager',
        'numpy',
        'us',
        'scipy',
        'pandas'
    ],
    author='Ryan Wendling',
    url='https://github.com/rd-wendling/rwend-tools',
)