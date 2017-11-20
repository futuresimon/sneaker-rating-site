#from the flask set up tutorial http://flask.pocoo.org/docs/0.12/tutorial/
from setuptools import setup

setup(
    name='sneakeragg',
    packages=['sneakeragg'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
